import numpy as np
import wxgen.util
import pywt
import datetime
import wxgen.variable
import wxgen.climate_model
import copy
import netCDF4
import time as timing


class Database(object):
   """
   Abstract class which stores weather segments (short time-series)

   The database is stored in self._data, which has dimensions (T, X, Y, V, N) where T is the segment
   length, V is the number of variables, N is the number of segments, and X and Y are geographical
   dimensions. A subclass must populate this field during initialization.

   Attributes:
      variables: A list of wxgen.variable.Variable
      length (int): Length of each trajectory (in number of days)
      num (int): Number of trajectories
      lats (np.array): 2D grid of latitudes
      lons (np.array): 2D grid of longitudes
      X (int): Number of X-axis points
      Y (int): Number of Y-axis points
      inittimes (np.array): array with initialization time corresponding to each member
      climate_states (np.array): array of climate states (one for each ensemble member)
      name: Name of this database (e.g. filename)

   Internal:
      data (np.array): A 5D array of data with dimensions (lead_time, lat, lon, variable, member*time)
      _data_agg (np.array): A 3D array of data with dimensions (lead_time, variable, member*time)
      _data_matching (np.array): A 3D array of data with dimensions (lead_time, variable, member*time)
   """
   def __init__(self, model=None):
      self._data_agg_cache = None
      self._data_matching_cache = None
      self.wavelet_levels = 0
      if model is None:
         self.model = wxgen.climate_model.Bin(10)
      else:
         self.model = model

   def info(self):
      print "Database information:"
      print "  Length of segments: %d" % self.length
      print "  Number of segments: %d" % self.num
      print "  Number of variables: %d" % len(self.variables)

   @property
   def name(self):
      """ Default to setting the name to the filename without the path """
      I = self.fullname.rfind('/')
      name = self.fullname[I + 1:]
      return name

   def get(self, i):
      """ Get the i'th trajectory in the database """
      indices = np.zeros([self.length, 2], int)
      indices[:, 0] = i
      indices[:, 1] = np.arange(0, self.length)
      assert(np.sum(np.isnan(indices)) == 0)
      return wxgen.trajectory.Trajectory(indices)

   def get_truth(self, start_date=None, end_date=None):
      """ Concatenate the initialization state of all trajectories """
      start = np.min(self.inittimes) if start_date is None else wxgen.util.date_to_unixtime(start_date)
      end = np.max(self.inittimes) if end_date is None else wxgen.util.date_to_unixtime(end_date)
      times = np.arange(start, end, 86400)
      indices = -1*np.ones([len(times), 2], int)
      wxgen.util.debug("Start: %d End: %d" % (start, end))
      for i in range(0, len(times)):
         time = times[i]
         I = np.where(time >= self.inittimes)[0]
         if len(I) == 0:
            wxgen.util.error("There are no inittimes available before %d. The earliest is %d." %
                  (wxgen.util.unixtime_to_date(time), wxgen.util.unixtime_to_date(
                     np.min(self.inittimes))))
         inittime = np.max(self.inittimes[I])
         lt = int((time - inittime)/86400)
         if lt < self.length:
            indices[i, 0] = np.where(self.inittimes == inittime)[0][0]
            indices[i, 1] = lt
         else:
            wxgen.util.warning("Did not find an index for %d = %d. Using the previous state." % (time, wxgen.util.unixtime_to_date(time)))
            assert(i > 0)
            indices[i, 0] = indices[i-1, 0]
            indices[i, 1] = indices[i-1, 1]

      return wxgen.trajectory.Trajectory(indices)

   def extract(self, trajectory):
      """
      Extract a trajectory of large-scale aggregated values from the database

      Arguments:
         trajectory (wxgen.trajectory.Trajectory): Trajectory to extract

      Returns:
         np.array: A 2D array (Time, variable) sequence of values
      """
      T = trajectory.indices.shape[0]
      V = len(self.variables)
      values = np.nan*np.zeros([T, V], float)
      for i in range(0, trajectory.indices.shape[0]):
         if trajectory.indices[i, 1] >= 0:
            values[i, :] = self._data_agg[trajectory.indices[i, 1], :, trajectory.indices[i, 0]]
      return values

   def extract_grid(self, trajectory):
      """
      Extract a trajectory of large-scale values from the database

      Arguments:
         trajectory (wxgen.trajectory.Trajectory): Trajectory to extract

      Returns:
         np.array: A 4D array (Time, X, Y, variable) sequence of values
      """
      T = trajectory.indices.shape[0]
      V = len(self.variables)
      X = self.X
      Y = self.Y
      if 1:
         values = np.nan*np.zeros([T, Y, X, V], float)
         # Loop over member, lead-time indices
         for i in range(0, trajectory.indices.shape[0]):
            m = trajectory.indices[i, 0]
            t = trajectory.indices[i, 1]
            assert(not np.isnan(m))
            assert(not np.isnan(t))
            if t >= 0:
               values[i, :, :, :] = self._data[t, :, :, :, m]
      else:
         # Slightly faster way (but not much faster)
         I0 = trajectory.indices[:, 0]
         I1 = trajectory.indices[:, 1]
         values = self._data[I1, :, :, :, I0]
      return values

   def extract_matching(self, trajectory):
      """
      Extract a trajectory of values used to match states from the database

      Arguments:
         trajectory (wxgen.trajectory.Trajectory): Trajectory to extract

      Returns:
         np.array: A 2D array (Time, variable) sequence of values
      """
      T = trajectory.indices.shape[0]
      values = np.nan*np.zeros([T, self._data_matching.shape[1]], float)
      for i in range(0, trajectory.indices.shape[0]):
         if trajectory.indices[i, 1] >= 0:
            values[i, :] = self._data_matching[trajectory.indices[i, 1], :, trajectory.indices[i, 0]]
      return values

   @property
   def _data_agg(self):
      if self._data_agg_cache is None:
         self._data_agg_cache = np.mean(np.mean(self._data, axis=2), axis=1)
      return self._data_agg_cache

   @property
   def _data_matching(self):
      if self._data_matching_cache is None:
         print "Loading from cache"
         if self.wavelet_levels == 0:
            self._data_matching_cache = self._data_agg
         else:
            # Decompose the grid
            s = timing.time()
            LT = self._data.shape[0]
            V = self._data.shape[3]
            M = self._data.shape[4]
            Nlat = self._data.shape[1]
            Nlon = self._data.shape[2]
            # data: lead_time, lat, lon, variable, member
            NX = np.ceil(float(Nlat)/2**self.wavelet_levels)
            NY = np.ceil(float(Nlon)/2**self.wavelet_levels)
            N = int(NX*NY)
            # print "Number of coefficients: %d" % N
            self._data_matching_cache = np.zeros([LT, V*N, M])
            for lt in range(self._data.shape[0]):
               for v in range(self._data.shape[3]):
                  for m in range(self._data.shape[4]):
                     # print "Computing wavelet for leadtime %d variable %d member %d" % (lt, v, m)
                     dec = pywt.wavedec2(self._data[lt, :, :, v, m], 'haar', level=self.wavelet_levels)[0]
                     dec = dec.flatten()/2**self.wavelet_levels
                     I = range(v*N, (v+1)*N)
                     self._data_matching_cache[lt, I, m] = dec
            e = timing.time()
            wxgen.util.debug("Wavelet time: %f" % (e - s))

            # print "Size of matching cache:", self._data_matching_cache.shape
      return self._data_matching_cache

   @property
   def X(self):
      return self._data.shape[2]

   @property
   def Y(self):
      return self._data.shape[1]

   def index2(self):
      pass


class Random(Database):
   """
   Trajectories are random Gaussian walks, with constant variance over time. There is no covariance
   between different forecast variables.
   """
   def __init__(self, N, T, V, variance=1, model=None):
      Database.__init__(self, model)
      self.num = N
      self.length = T
      if V is None:
         V = 1
      self._V = V
      self._variance = variance
      self._data = np.zeros([T, 1, 1, V, N], float)
      self.fullname = "Random(%d,%d,%d)" % (N, T, V)

      # Ensure that the signal has a constant variance over time
      scale = 1./np.sqrt(np.linspace(1, T, T))

      for v in range(0, self._V):
         self._data[:, 0, 0, v, :] = np.transpose(np.resize(scale, [N, T])) * np.cumsum(np.random.randn(T, N) * np.sqrt(self._variance), axis=0)

      self.variables = [wxgen.variable.Variable("var%d" % i) for i in range(0, self._V)]
      self.lats = np.zeros([1, 1])
      self.lons = np.zeros([1, 1])
      self.climate_states = np.mod(np.arange(0, N), 12)
      for i in range(N):
          self._data[:, :, :, :, i] += np.cos(self.climate_states[i] / 12.0 * 2 * 3.14159265) * -3
      start = wxgen.util.date_to_unixtime(20150101)
      num_inits = 30
      self.inittimes = start + np.mod(np.arange(0, N), num_inits) * 86400


class Netcdf(Database):
   """
   Segments stored in a netcdf database. This can either be an aggregated or a gridded database.

   Aggregated database has the following format:
      dims: forecast_reference_time, time, ensemble_member
      vars: forecast_reference_time(forecast_reference_time), time(time)
            variable_name(forecast_reference_time, time, ensemble_member)

   Gridded database has the following format:
      dims: forecast_reference_time, lat(itude), lon(gitude), time, ensemble_member
      vars: forecast_reference_time(forecast_reference_time), time(time)
            variable_name(forecast_reference_time, time, member, latitude, longitude)

   where variable_name is one or more names of weather variables. Forecast_reference_time is
   optional, i.e. both the variable and dimension could be missing.
   """
   def __init__(self, filename, vars=None, model=None):
      """
      Arguments:
         filename (str): Load data from this file
         vars (list): List of indices for which variables to use
      """
      Database.__init__(self, model)
      self.fullname = filename
      self._file = netCDF4.Dataset(filename)

      self._initname = "forecast_reference_time"

      # Set dimensions
      var_names = [name for name in self._file.variables if name not in ["lat", "lon", "latitude", "longitude", "x", "y", "ensemble_member", "time", "dummy", "longitude_latitude", "forecast_reference_time", "projection_regular_ll"]]
      if vars is None:
         vars = range(len(var_names))

      if vars is not None and max(vars) >= len(var_names):
         wxgen.util.error("Index in --vars (%d) is >= number of variables (%d)" % (max(vars), len(var_names)))

      self.variables = list()
      for i in vars:
         var_name = var_names[i]
         units = None
         label = None
         dims = self._file.variables[var_name].dimensions
         if "time" in dims:
            if hasattr(self._file.variables[var_name], "units"):
               units = self._file.variables[var_name].units
            if hasattr(self._file.variables[var_name], "standard_name"):
               label = self._file.variables[var_name].standard_name
            var = wxgen.variable.Variable(var_name, units, label)
            self.variables.append(var)
            wxgen.util.debug("Using variable '%s'" % var_name)

      # Load data
      self.length = self._file.dimensions["time"].size
      self._members = self._file.dimensions["ensemble_member"].size
      V = len(self.variables)
      M = self._members
      has_frt = True
      if "forecast_reference_time" in self._file.dimensions:
         D = self._file.dimensions["forecast_reference_time"].size
      else:
         D = 1
         has_frt = False
      times = self._file.variables[self._initname][:]
      if len(times.shape) == 0:
         times = np.array([times])

      Itimes = np.where(np.isnan(times) == 0)[0]
      times = times[Itimes]
      D = len(times)
      T = self.length

      # Read lat/lon dimensions
      is_spatial = True
      if "lon" in self._file.dimensions:
         X = self._file.dimensions["lon"].size
         Y = self._file.dimensions["lat"].size
      elif "longitude" in self._file.dimensions:
         X = self._file.dimensions["longitude"].size
         Y = self._file.dimensions["latitude"].size
      elif "x" in self._file.dimensions:
         X = self._file.dimensions["x"].size
         Y = self._file.dimensions["y"].size
      else:
         is_spatial = False
         X = 1
         Y = 1
         self.lats = np.zeros([1, 1])
         self.lons = np.zeros([1, 1])

      # Read lat/lon variables
      if is_spatial:
         if "lat" in self._file.variables:
            self.lats = self._copy(self._file.variables["lat"])
            self.lons = self._copy(self._file.variables["lon"])
         elif "latitude" in self._file.variables:
            self.lats = self._copy(self._file.variables["latitude"])
            self.lons = self._copy(self._file.variables["longitude"])
         if len(self.lats.shape) == 1 or self.lats.shape[1] == 1:
            wxgen.util.debug("Meshing latitudes and longitudes")
            # [self.lats, self.lons] = np.meshgrid(self.lats, self.lons)
            [self.lons, self.lats] = np.meshgrid(self.lons, self.lats)

      self.num = M * D
      wxgen.util.debug("Allocating %.2f GB" % (T*Y*X*V*M*D*4.0/1024/1024/1024))
      self._data = np.nan*np.zeros([T, Y, X, V, M*D], float)
      self._date = np.zeros(self.num, float)

      for v in range(0, V):
         var = self.variables[v]
         temp = self._copy(self._file.variables[var.name])  # dims: D, T, M, X, Y

         # Quality control
         if var.name == "precipitation_amount":
            temp[temp < 0] = 0
         index = 0
         for d in range(0, D):
            for m in range(0, M):
               if is_spatial:
                  if has_frt:
                     self._data[:, :, :, v, index] = temp[Itimes[d], :, m, :, :]
                  else:
                     self._data[:, :, :, v, index] = temp[:, m, :, :]
               else:
                  if has_frt:
                     self._data[:, :, :, v, index] = np.reshape(temp[Itimes[d], :, m], [T, Y, X])
                  else:
                     self._data[:, :, :, v, index] = np.reshape(temp[:, m], [T, Y, X])
               index = index + 1

      # If one or more values are missing for a member, set all values to nan
      for e in range(0, M*D):
         NM = np.sum(np.isnan(self._data[:, :, :, :, e]))
         if NM > 0:
            self._data[:, :, :, :, e] = np.nan
            wxgen.util.debug("Removing member %d because of %d missing values" % (e, NM))

      self.inittimes = np.repeat(times, self._members)

      self.climate_states = self.model.get(self.inittimes)
      self._file.close()

   def _copy(self, data):
      data = data[:].astype(float)
      q = copy.deepcopy(data)
      # Remove missing values. Convert to -999 and then back to nan to avoid
      # warning messages when doing <, >, and == comparisons with nan.
      q[np.isnan(q)] = -999
      q[(q == -999) | (q < -1000000) | (q > 1e30)] = np.nan
      return q


class Lorenz63(Database):
   """
   Trajectories based on the Lorenz 63 model.
   """
   def __init__(self, N, T, R=28, S=10, B=2.6667, dt=0.0001, model=None):
      Database.__init__(self, model)
      self.num = N
      self.length = T
      self._R = R
      self._S = S
      self._B = B
      self._dt = dt
      self._V = 3  # Number of variables
      self._data = np.zeros([T, 1, 1, self._V, N], float)
      self.lats = np.zeros([1, 1])
      self.lons = np.zeros([1, 1])
      self._initial_state = [-10, -10, 25]
      self._std_initial_state = 0.1  # Standard deviation of initial condition error

      # Initialize
      for v in range(0, self._V):
         self._data[0, 0, 0, v, :] = self._initial_state[v] + np.random.randn(N) * self._std_initial_state

      TT = int(1 / self._dt)/10
      # Iterate
      for t in range(1, T):
         x0 = copy.deepcopy(self._data[t-1, 0, 0, 0, :])
         y0 = copy.deepcopy(self._data[t-1, 0, 0, 1, :])
         z0 = copy.deepcopy(self._data[t-1, 0, 0, 2, :])
         # Iterate from t-1 to t
         for tt in range(0, TT):
            x1 = x0 + self._dt * self._S * (y0 - x0)
            y1 = y0 + self._dt * (self._R * x0 - y0 - (x0 * z0))
            z1 = z0 + self._dt * (x0*y0 - self._B*z0)

            x2 = x1 + self._dt * self._S * (y1 - x1)
            y2 = y1 + self._dt * (self._R * x1 - y1 - x1*z1)
            z2 = z1 + self._dt * (x1*y1 - self._B*z1)

            x0 = 0.5 * (x2 + x0)
            y0 = 0.5 * (y2 + y0)
            z0 = 0.5 * (z2 + z0)

         self._data[t, 0, 0, 0, :] = x0
         self._data[t, 0, 0, 1, :] = y0
         self._data[t, 0, 0, 2, :] = z0

      self.variables = [wxgen.variable.Variable(i) for i in ["X", "Y", "Z"]]
      self.fullname = "Lorenz(%d,%d,%f,%f,%f)" % (N, T, R, S, B)
