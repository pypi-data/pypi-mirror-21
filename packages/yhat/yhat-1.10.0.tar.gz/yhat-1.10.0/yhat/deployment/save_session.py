try:
    from .models import SplitTestModel
except ImportError:
    from models import SplitTestModel
from builtins import str as text
import pickle
import terragon
import ast
import inspect
import tokenize
import types
import json
import sys
import re
import io
import os
import pprint as pp
from .reindenter import Reindenter
import logging


try:
    import dill
except:
    pass

def reindent(code):
    code = u"%s" % text(code)
    r = Reindenter(io.StringIO(code))
    r.run()
    out = io.StringIO()
    r.write(out)
    return out.getvalue()


def _in_directory(filepath, directory):
    #make both absolute
    directory = os.path.realpath(directory)
    filepath = os.path.realpath(filepath)
    #return true, if the common prefix of both is equal to directory
    #e.g. /a/b/c/d.rst and directory is /a/b, the common prefix is /a/b
    return os.path.commonprefix([filepath, directory]) == directory

def _is_on_syspath(filepath):
    if filepath is None:
        return False
    for libpath in sys.path:
        if libpath==os.getcwd():
            continue
        elif libpath!="":
            if _in_directory(filepath, libpath)==True:
                return True

    if os.environ.get("CONDA_DEFAULT_ENV"):
        # CONDA wierdness. check and see if CONDA is messing with our
        # syspath we're also going to have an exception for the yhat
        # library. not sure if this actually helps/hurts, but I don't
        # want to find out
        conda_env = os.environ["CONDA_DEFAULT_ENV"]
        conda_syspath = os.path.join(conda_env, "lib", "python2.7")
        if conda_syspath in filepath:
            return True

    if os.environ.get("VIRTUAL_ENV"):
        # same nonsense as above,but for virtualenv
        if _in_directory(filepath, os.environ["VIRTUAL_ENV"]):
            return True

    return False

def _get_source_inspect_or_dill(obj):
    try:
        return inspect.getsource(obj)
    except Exception as e:
        return dill.source.getsource(obj)

def _get_source(func):
    """
    Gets the source of a function and handles cases when user is in an
    interactive session

    func: function
        a function who's source we want
    """
    # standardize source code indent to 4 spaces
    return reindent(_get_source_no_reindent(func))

def _get_source_no_reindent(func):
    try:
        return _get_source_inspect_or_dill(func)
    except:
        if inspect.isclass(func):
            source = ""
            source += "class %s(%s):" % (func.__name__, func.__base__.__name__)
            source += "\n"
            for name, method in inspect.getmembers(func, predicate=inspect.ismethod):
                if hasattr(method, '__wrapped_func__'):
                    wrapped_source = _get_source_inspect_or_dill(method.__wrapped_func__)
                    wrapped_source = wrapped_source.split('\n')
                    nchar = len(wrapped_source[1]) - len(wrapped_source[1].lstrip())
                    wrapped_source[0] = " "*nchar + wrapped_source[0]
                    wrapped_source = "\n".join(wrapped_source)
                    wrapped_source = "\n" + reindent(wrapped_source) + "\n"
                    source += wrapped_source
                else:
                    try:
                        source += reindent(_get_source_inspect_or_dill(method)) + "\n"
                    except IOError as e:
                        msg = """Could not get the source code from your model. This is likely
becasue you're in an interactive Python session and have pasted
code directly into the console. In this situation, Python sometimes
adds additional whitespace which breaks the source code extraction.
Try running your code from an file instead.""".replace("\n", " ")
                        raise Exception(msg)
                    except Exception as e:
                        raise e
        else:
            try:
                return _get_source_inspect_or_dill(func) + "\n"
            except IOError as e:
                msg = """Could not get the source code from your model. This is likely
becasue you're in an interactive Python session and have pasted
code directly into the console. In this situation, Python sometimes
adds additional whitespace which breaks the source code extraction.
Try running your code from an file instead.""".replace("\n", " ")
                raise Exception(msg)
            except Exception as e:
                raise e
        return source


def _strip_function_source(src):
    """
    Takes the source code of a function and dedents it so that it.

    Parameters
    ----------
    src: string
        function code

    Returns
    -------
    source: string
        source code of the same function, but "dedented"
    """
    src = reindent(src)
    src = src.split('\n')
    n = len(src[0]) - len(src[0].lstrip())
    return "\n".join([line[n:] for line in src])

def _get_naked_loads(function):
    """
    Takes a reference to a function and determines which variables used in the
    function are not defined within the scope of the function.

    Parameters
    ----------
    function: function

    Returns
    -------
    variables: generator
        returns the variables in a function that are not:
            1) passed in as parameters
            2) created within the scope of the function
    """
    source = _get_source(function)
    source = _strip_function_source(source)
    logging.info("parsing source for %s\n" % str(function))
    logging.debug("%s\n" % source)
    tree = ast.parse(source)
    params = set()
    loaded = set()
    created = set()
    for thing in ast.walk(tree):
        thingvars = vars(thing)
        if "ctx" in thingvars:
            if isinstance(thingvars['ctx'], ast.Param):
                params.add(thingvars['id'])
            elif isinstance(thingvars['ctx'], ast.Load):
                if 'id' in thingvars:
                    loaded.add(thingvars['id'])
                    # variable = thingvars['id']
                    # if variable not in params and variable not in created:
                        # yield variable
            elif isinstance(thingvars['ctx'], ast.Store):
                if 'id' in thingvars:
                    created.add(thingvars['id'])

    for variable in loaded:
        # TODO: if created but loaded before that as something else
        if variable not in params and variable not in created:
            yield variable

def _extract_module(module_name, modules={}):
    logging.debug("\textracting module %s." % module_name)
    module = sys.modules.get(module_name)
    # check if we've already seen it
    if module in modules or module is None:
        logging.debug("\tmodule %s was None, returning." % module_name)
        return modules
    # make sure it's not a built in module
    elif hasattr(module, "__file__")==False:
        logging.debug("\tmodule %s did not have a `__file__` attribute, returning." % module_name)
        return modules
    elif _is_on_syspath(module.__file__)==False:
        logging.debug("\tfile being parsed is: %s\n" % module.__file__)

        if module.__file__.endswith(".py"):
            module_py = module.__file__
        elif module.__file__.endswith(".pyc"):
            module_py = module.__file__.replace(".pyc", ".py")
        else:
            logging.debug("\t%s is not a .py or .pyc skipping and returning: \n" % module.__file__)
            modules[module_name] = None
            return modules

        with open(module_py, 'rb') as f:
            module_source = f.read()
        parent_dir = module_py.replace(os.getcwd(), '').lstrip(os.sep)
        parent_dir = os.path.dirname(parent_dir)
        modules[module] = {
            "parent_dir": parent_dir,
            "name": os.path.basename(module_py),
            "source": module_source
        }
        # Try to extract init files
        finit = os.path.join(parent_dir, "__init__.py")
        if os.path.isfile(finit):
            with open(finit, 'rb') as f:
                init_source = f.read()
                modules['init'] = {
                    "parent_dir": parent_dir,
                    "name": "__init__.py",
                    "source": init_source
                }

        logging.info("\tparsing source for %s\n" % module_name)
        logging.debug("%s\n" % module_source)

        logging.debug("\tparsing module source code for %s and looking for other modules to extract" % module_name)
        tree = ast.parse(module_source)
        for thing in ast.walk(tree):
            if hasattr(thing, "module"):
                modules.update(_extract_module(thing.module))
            elif isinstance(thing, (ast.Import, ast.ImportFrom)):
                for imp in thing.names:
                    if imp.name!="*":
                        modules.update(_extract_module(imp.name))
    else:
        modules[module_name] = None
    return modules

def _is_tensor(obj):
    try:
        return obj.__module__.startswith("tensorflow")
    except:
        try:
            return None != re.search( r'(tensorflow)', str(obj.__class__))
        except:
            return False

def _is_spark(obj):
    try:
        return obj.__module__.startswith("pyspark")
    except:
        try:
            return None != re.search( r'(pyspark)', str(obj.__class__))
        except:
            return False

def _is_pom(obj):
    try:
        return obj.__module__.startswith("pomegranate")
    except:
        try:
            return None != re.search( r'(pomegranate)', str(obj.__class__))
        except:
            return None

def _spider_function(function, session, pickles={}):
    """
    Takes a function and global variables referenced in an environment and
    recursively finds dependencies required in order to execute the function.
    This includes references to classes, libraries, variables, functions, etc.

    Parameters
    ----------
    function: function
        a function referenced in an environment
    session: dictionary
        variables referenced from a seperate environment; i.e. globals()
    pickles: dictionary
        holds the variables needed to execute the function

    Returns
    -------
    imports: list
        list of import statements required for the function to execute
    source: string
        source code of the function
    pickles: dictionary
        dictionary of variable names and their values as pickled strings
    """

    if '_objects_seen' not in pickles:
        pickles['_objects_seen'] = []
    pickles['_objects_seen'].append(str(function))
    imports = []
    modules = {}
    source = "# code for %s\n" % (str(function))
    if isinstance(function, types.ModuleType):
        logging.debug("object (%s) is a `types.ModuleType`. skipping _get_source" % str(function))
        pass
    else:
        source += _get_source(function) + '\n'

    logging.debug("finding objects that need to be serialized")
    for varname in _get_naked_loads(function):
        logging.debug("\t%s" % varname)
        if varname in pickles['_objects_seen']:
            logging.debug("\t%s has already been processed. skipping." % varname)
            continue
        pickles['_objects_seen'].append(varname)
        if varname not in session:
            logging.debug("\t%s not found in session. skipping." % varname)
            continue
        obj = session[varname]
        # checking to see if this is an instance of an object
        if hasattr(obj, "__name__")==False:
            logging.debug("\t%s has attribute __name__, performing serialization checks." % varname)
            if _is_tensor(obj):
                logging.debug("\t%s is from tensorflow skipping." % varname)
                continue
            elif _is_spark(obj):
                logging.debug("\t%s is from spark. serializing using `dumps_spark_to_base64`." % varname)
                pickles[varname] = terragon.dumps_spark_to_base64(session['sc'], obj)
            elif _is_pom(obj):
                logging.debug("\t%s is from pomegranate. serializing using `dumps_pom_to_base64`." % varname)
                pickles[varname] = terragon.dumps_pom_to_base64(obj)
            else:
                logging.debug("\tno special serialization requirement detected for %s. using dumps_to_base64." % varname)
                pickles[varname] = terragon.dumps_to_base64(obj)

        elif hasattr(obj, "__module__"):
            logging.debug("\tobject %s has attribute __module__" % varname)
            if obj.__module__=="__main__":
                logging.debug("\t%s is in module __main__" % varname)
                new_imports, new_source, new_pickles, new_modules = _spider_function(obj, session, pickles)
                source += new_source + '\n'
                imports += new_imports
                pickles.update(new_pickles)
                modules.update(new_modules)
            else:
                logging.debug("\t%s is a submodule (not __main__). extracting/saving source code and import statements." % varname)
                modules.update(_extract_module(obj.__module__))
                ref = inspect.getmodule(obj).__name__
                if hasattr(obj, "func_name") and obj.__name__!=varname:
                    imports.append("from %s import %s as %s" % (ref, obj.__name__, varname))
                else:
                    # we need to figure out how to import this library. i'm not
                    # sure exactly what the right way to get the module and
                    # class name, but this works just fine
                    try:
                        import_statement = "from %s import %s" % (ref, varname)
                        exec(import_statement, locals())
                        imports.append(import_statement)
                    except:
                        try:
                            import_statement = "from %s import %s" % (ref, obj.__class__.__name__)
                            exec(import_statement, locals())
                            imports.append(import_statement)
                        except:
                            pass

        elif isinstance(obj, types.ModuleType):
            logging.debug("\tobject %s is a `types.ModuleType`, extracting/saving source code and import statements." % varname)
            modules.update(_extract_module(obj.__name__))
            if obj.__name__!=varname:
                imports.append("import %s as %s" % (obj.__name__, varname))
            else:
                imports.append("import %s" % (varname))
        else:
            logging.debug("\tno special cases detected for %s. pickling using dumps_to_base64" % varname)
            # catch all. if all else fails, pickle it
            pickles[varname] = terragon.dumps_to_base64(obj)

    return imports, source, pickles, modules

def _detect_future_imports(session):
    """
    Detect all __future__ imports. Since these imports must come first in
    the source code, these are attempt to be detected outside of other
    spidering.

    Parameters
    ----------
    session: dictionary
        globals() from the user's environment
    """
    imports = []
    for k in list(session.keys()):
        v = session[k]
        if hasattr(v,"__module__"):
            if v.__module__ == "__future__":
                if k is 'print_function':
                    continue
                if not k.startswith('_'):
                    imports.append("from __future__ import %s" % k)
    return imports

def save_function(function, session):
    """
    Saves a user's session and all dependencies to a big 'ole JSON object with
    accompanying pickles for any variable.

    Parameters
    ----------
    function: function
        function we're saving
    session: dictionary
        globals() from the user's environment
    """

    future_imports = "\n".join(_detect_future_imports(session))
    logging.debug("Detecting future import for session. Found %s" % future_imports)

    logging.debug("Spidering model class %s" % str(function))
    imports, source_code, pickles, modules = _spider_function(function, session)

    # de-dup and order the imports
    imports = sorted(list(set(imports)))

    imports.append("import random") # we need this for the execute method for a SplitTestModel
    imports.append("import json")
    imports.append("import pickle")
    imports.append("import terragon")
    source_code = "\n".join(imports) + "\n\n\n" + source_code
    pickModules = []

    logging.debug("%d sub-modules found. encoding source code as utf-8." % len(modules))
    for _, value in list(modules.items()):
        if value is not None:
            try:
                value['source'] = value['source'].decode(encoding="utf-8")
                pickModules.append(value)
            except Exception as e:
                logging.debug("could not encode source for %s: %s" % (str(value), str(e)))
                pickModules.append(value)

    pickles = {
        "objects": pickles,
        "future": future_imports,
        "code": source_code,
        "modules": pickModules
    }

    logging.debug("Future Imports Found: %s" % str(future_imports))
    logging.debug("Objects Found: %s" % str(pickles.keys()))
    logging.debug("Source Code Found:\n%s" % source_code)
    logging.debug("Modules Found:\n%s" % pp.pformat(pickModules, indent=2))

    if "_objects_seen" in pickles["objects"]:
        del pickles["objects"]["_objects_seen"]
    return pickles
