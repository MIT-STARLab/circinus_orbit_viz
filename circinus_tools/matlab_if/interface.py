import time

# For matlab setup, see http://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html?refresh=true
import matlab
from matlab import engine

MATLAB_OPTIONS = "-nojvm -nodesktop -nosplash -r matlab.engine.shareEngine"
DEFAULT_EXISTING_ENGINE_INDX = -1

class MatlabIF:
    """
    Provides an elegant wrapper around MATLAB python interface functionality

    Tested with MATLAB 2017a, Python 3.5.4

    Note that if new persistent matlab instances are created, clean_up_persistent_engines() should eventually be called to close them. Can be called either in the same python kernel instance, or a subsequent instance. These instances can also be accessed from outside python through the interface of the daemon being used. e.g., "screen -ls; screen -r MATLAB_INSTANCE_NAME"

    See here for general matlab-python usage details: https://www.mathworks.com/help/matlab/matlab-engine-for-python.html
    See here for info about handling data returned from matlab: https://www.mathworks.com/help/matlab/matlab_external/handle-data-returned-from-matlab-to-python.html
    """

    def __init__(self,matlab_ver='MATLAB_R2017a',paths=[],connect=True,use_existing=True,persistent=True):
        self.eng = None
        self.eng_name = None
        self.eng_deleted = False
        self.matlab_ver = matlab_ver

        # to run persistent matlab instances, we'll use screen as a daemon
        self.daemon = 'screen'

        if connect:
            self._connect_matlab_engine(use_existing,persistent)

        if paths:
            self.add_paths(paths)

    def add_paths(self,paths):
        """
        Add paths in which matlab engine should search for scripts

        :param paths: str or list of strings containing path or multiple paths, repspectively
        :return:
        """
        if self.eng:
            if type(paths) is str:
                self.eng.addpath(paths)
            elif type(paths) is list:
                for path in paths:
                    self.eng.addpath(path)

    @staticmethod
    def get_existing_eng_names():
        return matlab.engine.find_matlab()

    @staticmethod
    def delete_matlab_engines(vars_dict):
        for item in vars_dict.items():
            mif = item[1]
            if type(mif) == MatlabIF:
                del mif.eng
                mif.eng_deleted = True

    @staticmethod
    def clean_up_persistent_engines(MatlabIF_instances={}, daemon='screen'):
        """
        Get rid of shared matlab engine instances after greping for their presence in ps -e

        Deletes the eng attribute of existing MatlabIF instances to ensure elegent cleanup, otherwise erroneous errors
        can be produced if MatlabIF objects get reused. Flags those instances with attribute eng_deleted = True

        Note: tried to play nice and use eng.exit() or eng.quit(), but that doesn't seem to work...

        :param list MatlabIF_instances: dict with all the MatlabIF instances that have been created in the current python kernel. Usually easiest to pass globals() here
        :param daemon: daemon used in this interface
        :return:
        """

        if daemon == 'screen':
            # this may work for other daemons too...

            MatlabIF.delete_matlab_engines(MatlabIF_instances)

            from subprocess import Popen, PIPE, call
            import re

            p1 = Popen(["ps","-e"], stdout=PIPE)
            p2 = Popen(["grep","matlab"], stdin=p1.stdout, stdout=PIPE)
            ps_out_lines = str.splitlines(p2.communicate()[0].decode("utf-8"))

            for line in ps_out_lines:
                if MATLAB_OPTIONS in line:
                    pids = re.findall('^[0-9]+', line, re.MULTILINE)

                    if len(pids) > 1:
                        raise Exception('only expected one pid match in this line')
                    else:
                        pid = pids[0]

                    # kill the matlab instance
                    # call(["kill", "-13", pid])
                    Popen(["kill", "-31",pid], stdout=PIPE)

            Popen(["screen", "-wipe"], stdout=PIPE)

        else:
            raise NotImplementedError

    @staticmethod
    def mlarray_to_list(m_arr,override= None,  arrayicize_singletons= False) :
        """
        Convert matlab array to python list

        important note: when an array with a single element is returned from  Matlab, it will not appear as an array in Python but rather as a single value. Obviously this behavior is frustrating, but that's life. This function assumes that such arrays should be left as singleton values      

        this function will return empty Matlab matrices as an empty Python list (if you don't want empty list to appear in your output, make sure to filter them before providing them to this function)

        :param m_arr: matlab array to convert
        :return: python list
        """

        #  not  implementing this capability for the time being
        if arrayicize_singletons:
            raise NotImplementedError

        elif isinstance(m_arr, int):
            return m_arr
        elif isinstance(m_arr, float):
            return m_arr

        elif override  and override=='flat_list':
            # print (m_arr)
            # get the size of the array/matrix
            width = m_arr.size[1]

            stuff = []

            for j in range(width):
                stuff.append (m_arr[0][j])

            return stuff

        else:
            # get the size of the array/matrix
            height = m_arr.size[0]
            width = m_arr.size[1]

            stuff = [[None for i in range(width)] for j in range(height)]

            for i in range(height):
                for j in range(width):
                    stuff[i][j] = m_arr[i][j]

            return stuff

    MATLAB_ARRAY_TYPES = [ matlab.double]

    @staticmethod
    def deep_convert_matlab_to_python (ml_stuff,matlab_nesting=None):
        """convert a Matlab formatted data structure to Python formatting.
          
        dig deep into the structure and convert Matlab numerical lists
           to Python

        :param ml_stuff:  Matlab struct to convert
        :param matlab_nesting: specification of how structure is nested 
            for conversion to Matlab. every pair of [] represents a cell 
            array  (note: cell arrays are automatically converted to lists
            when the data is passed from Matlab to Python)
        :return: python list
        """

        # need to add these checks because...MATLAB. When it returns a one element int/double array, that "array" is in actuality just an integer/double basic data type.
        if matlab_nesting and matlab_nesting  == 'value':
            return MatlabIF.mlarray_to_list (ml_stuff, override='value')
            # return ml_stuff
        elif isinstance(ml_stuff, int):
            return [ml_stuff]
        elif isinstance(ml_stuff, float):
            return [ml_stuff]

        # check first whether we're supposed to stop at this level of nesting and turn it into a Matlab matrix structure
        elif matlab_nesting and matlab_nesting  == 'flat_list':
            return MatlabIF.mlarray_to_list (ml_stuff, override='flat_list')

        elif type(ml_stuff) in MatlabIF.MATLAB_ARRAY_TYPES:
            return MatlabIF.mlarray_to_list (ml_stuff)

        elif isinstance(ml_stuff,list):            
            next_nesting= matlab_nesting[0] if matlab_nesting else None
            return [ MatlabIF.deep_convert_matlab_to_python (elem,next_nesting) for elem in ml_stuff]

        else:
            print (ml_stuff)
            print ( type (ml_stuff))
            raise NotImplementedError

    @staticmethod
    def deep_convert_python_to_matlab (python_stuff,matlab_nesting=None,blind_convert=False):
        """convert a python  data structure to the correct formatting for Matlab. Essentially, it just converts numbers over to Matlab double matrices. The conversion of everything else the Matlab API will handle itself: dicts -> structs, strings -> matlab strings, lists -> matrices...

        :param python_stuff:  Matlab struct to convert
        :param matlab_nesting: specification of how structure is nested 
            for conversion to Matlab. every pair of [] represents a cell 
            array  (note: lists are automatically converted to cell arrays  
            when the data is given to Matlab)
        :param blind_convert:  anything that we can convert to Matlab we'll do immediately. This should be used, for example, to convert a dict containing a number matrix (nested list of lists containing floats) to a matlab double.  if any other lists are present  that cannot be directly converted using matlab.double, conversion will break
        :return: python list
        """

        if matlab_nesting and blind_convert:
            raise Exception('matlab_nesting and blind_convert options should not be used at the same time')

        #  converting integers and floats
        if isinstance(python_stuff, int) or isinstance(python_stuff, float):
            return matlab.double([python_stuff])

            # #  for blindly converting, return the Matlab double version
            # if blind_convert_number: return matlab.double([python_stuff])
            # #  otherwise return the Python version
            # else: return python_stuff

        elif isinstance(python_stuff, str) or isinstance(python_stuff, bool):
            return python_stuff

        elif isinstance(python_stuff,list):
            # check first whether we're supposed to stop at this level of nesting and turn it into a Matlab matrix structure
            #  blind convert will always convert. We can handle  a nested list of lists of numbers
            #  nesting will only convert if we've specified to convert at this level
            if blind_convert or (matlab_nesting and matlab_nesting  == matlab.double):
                return matlab.double(python_stuff)
            # check if it's a nested list, if yes continue deeper
            elif any(isinstance(i, list) or isinstance(i, dict) or isinstance(i, str) for i in python_stuff):
                next_nesting= matlab_nesting[0] if matlab_nesting else None
                return [ MatlabIF.deep_convert_python_to_matlab(elem,next_nesting) for elem in python_stuff]
            
            #  if we reach here then we have a plain list to convert
            else:
                return matlab.double(python_stuff)

        elif isinstance(python_stuff,dict):
            if matlab_nesting:
                raise NotImplementedError

            def invalid_key(key):
                if type(key) == str:
                    if key[0] == '_':
                        return True

                return False

            return {key: MatlabIF.deep_convert_python_to_matlab(value,blind_convert=blind_convert) for key, value in python_stuff.items() if not invalid_key(key)}

        else:
            raise NotImplementedError

    def get_matlab_bin_path(self):
        from sys import platform

        # OS X
        if platform == "darwin":
            return "/Applications/" + self.matlab_ver + ".app/bin/matlab"
        else:
            raise NotImplementedError


    def _start_persistent_shared_matlab(self):
        from os import system
        from datetime import datetime

        previous_sessions_tup = engine.find_matlab()

        if self.daemon == 'screen':
            session_name = 'matlab_' + datetime.utcnow().isoformat()
            # start matlab in detached screen session and run command to share the session
            system('screen -dmS ' + session_name + ' ' + self.get_matlab_bin_path() + " " + MATLAB_OPTIONS)
        else:
            raise NotImplementedError


        # wait till we see a new shared matlab sesh
        new_sessions_tup = engine.find_matlab()
        while (new_sessions_tup == previous_sessions_tup):
            time.sleep(1)
            new_sessions_tup = engine.find_matlab()

        return new_sessions_tup[-1]

    def _connect_matlab_engine(self,use_existing=True,persistent=True):
        """
        Connect to a matlab engine, starting a new one if it hasn't been started yet

        :return:
        """

        found_eng = False
        if use_existing:
            eng_names = engine.find_matlab()
            for eng_name in eng_names:
                try:
                    self.eng = engine.connect_matlab(eng_name)
                    self.eng_name = eng_name
                    found_eng = True

                # unable to connect to an instance because it already has a connection
                except matlab.engine.EngineError:
                    pass

                if found_eng:
                    break

        if not found_eng:
            # if we're making a new persistent engine, create it
            if persistent:
                self.eng_name = self._start_persistent_shared_matlab()
                self.eng = engine.connect_matlab(self.eng_name)

            # otherwise, make a new engine just for the lifetime of self
            else:
                self.eng = engine.start_matlab()
                self.eng_name = None # to be explicit

        self.eng_deleted = False

    def call_mfunc(self,mfunc_name,*args, **kwargs):
        """
        Call a matlab function, passing *args to it as the standard matlab function arguments

        See here: https://www.mathworks.com/help/matlab/matlab_external/pass-data-to-matlab-from-python.html
        and here: https://www.mathworks.com/help/matlab/matlab_external/handle-data-returned-from-matlab-to-python.html
        for info on converting between python and matlab data types.

        :param mfunc_name: name of the function. Should be in the paths already added to self
        :param args: the arguments to pass to with the function call in matlab. Can be either matlab or python format, depends on context.
        :param kwargs: kwargs to pass to the MatlabFunc interface (matlabengine.py in matlab.engine package)
        :return: tuple of values returned from matlab, in matlab format.
        """

        # TODO: someday it would be good to add better validation of *args to make sure they match what matlab expects...I don't think matlab does this very elegantly. Would also fix the non one-to-one output type mapping

        if not type(mfunc_name) == str:
            raise TypeError('mfunc_name should be of type string')

        return self.eng.feval(mfunc_name,*args,**kwargs)

    @staticmethod
    def convert_matlab_indexing_to_python(mat):
        """Convert a matrix with Matlab 1-based indexing to 0-based
        
        [description]
        :param mat: [description]
        :type mat: [type]
        :returns: [description]
        :rtype: {[type]}
        :raises: NotImplementedError
        """
        if type (mat)==  list:
            converted = [MatlabIF.convert_matlab_indexing_to_python(elem) for elem in mat]
        elif  type (mat)== int:
            converted = mat-1
        else:
            raise NotImplementedError    

        return converted


if __name__ == "__main__":
    mif = MatlabIF(use_existing=True)
    # mif = MatlabIF(use_existing=False,persistent=True)

    # del mif
    # mif = MatlabIF(connect=False)
    # mif.clean_up_persistent_engines()

