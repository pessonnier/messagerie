```
(cv) pi@pi3:~/prog/dlib $ python setup.py install --compiler-flags "-mfpu=neon"
running install
running bdist_egg
running build
Detected Python architecture: 32bit
Detected platform: linux
Removing build directory /home/pi/prog/dlib/./tools/python/build
Configuring cmake ...
-- The C compiler identification is GNU 4.9.2
-- The CXX compiler identification is GNU 4.9.2
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
CMake Warning at /usr/share/cmake-3.6/Modules/FindBoost.cmake:1475 (message):
  No header defined for python-py34; skipping header check
Call Stack (most recent call first):
  /home/pi/prog/dlib/dlib/cmake_utils/add_python_module:61 (FIND_PACKAGE)
  CMakeLists.txt:6 (include)
-- Boost version: 1.55.0
-- Found the following Boost libraries:
--   python-py34
-- Found PythonLibs: /usr/lib/arm-linux-gnueabihf/libpython3.4m.so (found suitable version "3.4.2", minimum required is "3.4")
-- USING BOOST_LIBS: /usr/lib/arm-linux-gnueabihf/libboost_python-py34.so
-- USING PYTHON_LIBS: /usr/lib/arm-linux-gnueabihf/libpython3.4m.so
-- C++11 activated.
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Looking for pthread_create
-- Looking for pthread_create - not found
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - found
-- Found Threads: TRUE
-- Looking for XOpenDisplay in /usr/lib/arm-linux-gnueabihf/libX11.so;/usr/lib/arm-linux-gnueabihf/libXext.so
-- Looking for XOpenDisplay in /usr/lib/arm-linux-gnueabihf/libX11.so;/usr/lib/arm-linux-gnueabihf/libXext.so - found
-- Looking for gethostbyname
-- Looking for gethostbyname - found
-- Looking for connect
-- Looking for connect - found
-- Looking for remove
-- Looking for remove - found
-- Looking for shmat
-- Looking for shmat - found
-- Looking for IceConnectionNumber in ICE
-- Looking for IceConnectionNumber in ICE - found
-- Found X11: /usr/lib/arm-linux-gnueabihf/libX11.so
-- Looking for png_create_read_struct
-- Looking for png_create_read_struct - found
-- Looking for jpeg_read_header
-- Looking for jpeg_read_header - found
-- Searching for BLAS and LAPACK
-- Found PkgConfig: /usr/bin/pkg-config (found version "0.28")
-- Checking for module 'cblas'
--   No package 'cblas' found
-- Checking for module 'lapack'
--   Found lapack, version 3.10.2
-- Looking for sys/types.h
-- Looking for sys/types.h - found
-- Looking for stdint.h
-- Looking for stdint.h - found
-- Looking for stddef.h
-- Looking for stddef.h - found
-- Check size of void*
-- Check size of void* - done
-- Found LAPACK library
-- Found ATLAS BLAS library
-- Looking for cblas_ddot
-- Looking for cblas_ddot - found
CUDA_TOOLKIT_ROOT_DIR not found or specified
-- Could NOT find CUDA (missing:  CUDA_TOOLKIT_ROOT_DIR CUDA_NVCC_EXECUTABLE CUDA_INCLUDE_DIRS CUDA_CUDART_LIBRARY) (Required is at least version "7.5")
-- *** cuDNN V5.0 OR GREATER NOT FOUND.  DLIB WILL NOT USE CUDA. ***
-- *** If you have cuDNN then set CMAKE_PREFIX_PATH to include cuDNN's folder.
-- Configuring done
-- Generating done
-- Build files have been written to: /home/pi/prog/dlib/tools/python/build
Build using cmake ...
Scanning dependencies of target dlib
[  1%] Building CXX object dlib_build/CMakeFiles/dlib.dir/base64/base64_kernel_1.cpp.o
[  2%] Building CXX object dlib_build/CMakeFiles/dlib.dir/bigint/bigint_kernel_1.cpp.o
[  4%] Building CXX object dlib_build/CMakeFiles/dlib.dir/bigint/bigint_kernel_2.cpp.o
[  5%] Building CXX object dlib_build/CMakeFiles/dlib.dir/bit_stream/bit_stream_kernel_1.cpp.o
[  6%] Building CXX object dlib_build/CMakeFiles/dlib.dir/entropy_decoder/entropy_decoder_kernel_1.cpp.o
[  8%] Building CXX object dlib_build/CMakeFiles/dlib.dir/entropy_decoder/entropy_decoder_kernel_2.cpp.o
[  9%] Building CXX object dlib_build/CMakeFiles/dlib.dir/entropy_encoder/entropy_encoder_kernel_1.cpp.o
[ 10%] Building CXX object dlib_build/CMakeFiles/dlib.dir/entropy_encoder/entropy_encoder_kernel_2.cpp.o
[ 12%] Building CXX object dlib_build/CMakeFiles/dlib.dir/md5/md5_kernel_1.cpp.o
[ 13%] Building CXX object dlib_build/CMakeFiles/dlib.dir/tokenizer/tokenizer_kernel_1.cpp.o
[ 14%] Building CXX object dlib_build/CMakeFiles/dlib.dir/unicode/unicode.cpp.o
[ 16%] Building CXX object dlib_build/CMakeFiles/dlib.dir/data_io/image_dataset_metadata.cpp.o
[ 17%] Building CXX object dlib_build/CMakeFiles/dlib.dir/data_io/mnist.cpp.o
[ 18%] Building CXX object dlib_build/CMakeFiles/dlib.dir/dnn/cpu_dlib.cpp.o
[ 20%] Building CXX object dlib_build/CMakeFiles/dlib.dir/dnn/tensor_tools.cpp.o
[ 21%] Building CXX object dlib_build/CMakeFiles/dlib.dir/sockets/sockets_kernel_1.cpp.o
[ 22%] Building CXX object dlib_build/CMakeFiles/dlib.dir/bsp/bsp.cpp.o
[ 24%] Building CXX object dlib_build/CMakeFiles/dlib.dir/dir_nav/dir_nav_kernel_1.cpp.o
[ 25%] Building CXX object dlib_build/CMakeFiles/dlib.dir/dir_nav/dir_nav_kernel_2.cpp.o
[ 27%] Building CXX object dlib_build/CMakeFiles/dlib.dir/dir_nav/dir_nav_extensions.cpp.o
[ 28%] Building CXX object dlib_build/CMakeFiles/dlib.dir/linker/linker_kernel_1.cpp.o
[ 29%] Building CXX object dlib_build/CMakeFiles/dlib.dir/logger/extra_logger_headers.cpp.o
[ 31%] Building CXX object dlib_build/CMakeFiles/dlib.dir/logger/logger_kernel_1.cpp.o
[ 32%] Building CXX object dlib_build/CMakeFiles/dlib.dir/logger/logger_config_file.cpp.o
[ 33%] Building CXX object dlib_build/CMakeFiles/dlib.dir/misc_api/misc_api_kernel_1.cpp.o
[ 35%] Building CXX object dlib_build/CMakeFiles/dlib.dir/misc_api/misc_api_kernel_2.cpp.o
[ 36%] Building CXX object dlib_build/CMakeFiles/dlib.dir/sockets/sockets_extensions.cpp.o
[ 37%] Building CXX object dlib_build/CMakeFiles/dlib.dir/sockets/sockets_kernel_2.cpp.o
[ 39%] Building CXX object dlib_build/CMakeFiles/dlib.dir/sockstreambuf/sockstreambuf.cpp.o
[ 40%] Building CXX object dlib_build/CMakeFiles/dlib.dir/sockstreambuf/sockstreambuf_unbuffered.cpp.o
[ 41%] Building CXX object dlib_build/CMakeFiles/dlib.dir/server/server_kernel.cpp.o
[ 43%] Building CXX object dlib_build/CMakeFiles/dlib.dir/server/server_iostream.cpp.o
[ 44%] Building CXX object dlib_build/CMakeFiles/dlib.dir/server/server_http.cpp.o
[ 45%] Building CXX object dlib_build/CMakeFiles/dlib.dir/threads/multithreaded_object_extension.cpp.o
[ 47%] Building CXX object dlib_build/CMakeFiles/dlib.dir/threads/threaded_object_extension.cpp.o
[ 48%] Building CXX object dlib_build/CMakeFiles/dlib.dir/threads/threads_kernel_1.cpp.o
[ 50%] Building CXX object dlib_build/CMakeFiles/dlib.dir/threads/threads_kernel_2.cpp.o
[ 51%] Building CXX object dlib_build/CMakeFiles/dlib.dir/threads/threads_kernel_shared.cpp.o
[ 52%] Building CXX object dlib_build/CMakeFiles/dlib.dir/threads/thread_pool_extension.cpp.o
[ 54%] Building CXX object dlib_build/CMakeFiles/dlib.dir/threads/async.cpp.o
[ 55%] Building CXX object dlib_build/CMakeFiles/dlib.dir/timer/timer.cpp.o
[ 56%] Building CXX object dlib_build/CMakeFiles/dlib.dir/stack_trace.cpp.o
[ 58%] Building CXX object dlib_build/CMakeFiles/dlib.dir/gui_widgets/fonts.cpp.o
[ 59%] Building CXX object dlib_build/CMakeFiles/dlib.dir/gui_widgets/widgets.cpp.o
[ 60%] Building CXX object dlib_build/CMakeFiles/dlib.dir/gui_widgets/drawable.cpp.o
[ 62%] Building CXX object dlib_build/CMakeFiles/dlib.dir/gui_widgets/canvas_drawing.cpp.o
[ 63%] Building CXX object dlib_build/CMakeFiles/dlib.dir/gui_widgets/style.cpp.o
[ 64%] Building CXX object dlib_build/CMakeFiles/dlib.dir/gui_widgets/base_widgets.cpp.o
[ 66%] Building CXX object dlib_build/CMakeFiles/dlib.dir/gui_core/gui_core_kernel_1.cpp.o
[ 67%] Building CXX object dlib_build/CMakeFiles/dlib.dir/gui_core/gui_core_kernel_2.cpp.o
[ 68%] Building CXX object dlib_build/CMakeFiles/dlib.dir/image_loader/png_loader.cpp.o
[ 70%] Building CXX object dlib_build/CMakeFiles/dlib.dir/image_saver/save_png.cpp.o
[ 71%] Building CXX object dlib_build/CMakeFiles/dlib.dir/image_loader/jpeg_loader.cpp.o
[ 72%] Building CXX object dlib_build/CMakeFiles/dlib.dir/image_saver/save_jpeg.cpp.o
[ 74%] Linking CXX static library libdlib.a
[ 74%] Built target dlib
Scanning dependencies of target dlib_
[ 75%] Building CXX object CMakeFiles/dlib_.dir/src/dlib.cpp.o
[ 77%] Building CXX object CMakeFiles/dlib_.dir/src/matrix.cpp.o
[ 78%] Building CXX object CMakeFiles/dlib_.dir/src/vector.cpp.o
[ 79%] Building CXX object CMakeFiles/dlib_.dir/src/svm_c_trainer.cpp.o
[ 81%] Building CXX object CMakeFiles/dlib_.dir/src/svm_rank_trainer.cpp.o
[ 82%] Building CXX object CMakeFiles/dlib_.dir/src/decision_functions.cpp.o
[ 83%] Building CXX object CMakeFiles/dlib_.dir/src/other.cpp.o
[ 85%] Building CXX object CMakeFiles/dlib_.dir/src/basic.cpp.o
[ 86%] Building CXX object CMakeFiles/dlib_.dir/src/cca.cpp.o
[ 87%] Building CXX object CMakeFiles/dlib_.dir/src/sequence_segmenter.cpp.o
[ 89%] Building CXX object CMakeFiles/dlib_.dir/src/svm_struct.cpp.o
[ 90%] Building CXX object CMakeFiles/dlib_.dir/src/image.cpp.o
[ 91%] Building CXX object CMakeFiles/dlib_.dir/src/rectangles.cpp.o
[ 93%] Building CXX object CMakeFiles/dlib_.dir/src/object_detection.cpp.o
[ 94%] Building CXX object CMakeFiles/dlib_.dir/src/shape_predictor.cpp.o
[ 95%] Building CXX object CMakeFiles/dlib_.dir/src/correlation_tracker.cpp.o
[ 97%] Building CXX object CMakeFiles/dlib_.dir/src/face_recognition.cpp.o
[ 98%] Building CXX object CMakeFiles/dlib_.dir/src/gui.cpp.o
[100%] Linking CXX shared library dlib.so
[100%] Built target dlib_
Install the project...
-- Install configuration: "Release"
-- Installing: /home/pi/prog/dlib/tools/python/../../python_examples/dlib.so
Populating the distribution directory /home/pi/prog/dlib/./dist/dlib ...
Copying file /home/pi/prog/dlib/./python_examples/face_recognition.py -> /home/pi/prog/dlib/./dist/dlib/examples/face_recognition.py.
Copying file /home/pi/prog/dlib/./python_examples/requirements.txt -> /home/pi/prog/dlib/./dist/dlib/examples/requirements.txt.
Copying file /home/pi/prog/dlib/./python_examples/max_cost_assignment.py -> /home/pi/prog/dlib/./dist/dlib/examples/max_cost_assignment.py.
Copying file /home/pi/prog/dlib/./python_examples/find_candidate_object_locations.py -> /home/pi/prog/dlib/./dist/dlib/examples/find_candidate_object_locations.py.
Copying file /home/pi/prog/dlib/./python_examples/face_detector.py -> /home/pi/prog/dlib/./dist/dlib/examples/face_detector.py.
Copying file /home/pi/prog/dlib/./python_examples/sequence_segmenter.py -> /home/pi/prog/dlib/./dist/dlib/examples/sequence_segmenter.py.
Copying file /home/pi/prog/dlib/./python_examples/train_shape_predictor.py -> /home/pi/prog/dlib/./dist/dlib/examples/train_shape_predictor.py.
Copying file /home/pi/prog/dlib/./python_examples/correlation_tracker.py -> /home/pi/prog/dlib/./dist/dlib/examples/correlation_tracker.py.
Copying file /home/pi/prog/dlib/./python_examples/face_landmark_detection.py -> /home/pi/prog/dlib/./dist/dlib/examples/face_landmark_detection.py.
Copying file /home/pi/prog/dlib/./python_examples/train_object_detector.py -> /home/pi/prog/dlib/./dist/dlib/examples/train_object_detector.py.
Copying file /home/pi/prog/dlib/./python_examples/dlib.so -> /home/pi/prog/dlib/./dist/dlib/dlib.so.
Copying file /home/pi/prog/dlib/./python_examples/svm_rank.py -> /home/pi/prog/dlib/./dist/dlib/examples/svm_rank.py.
Copying file /home/pi/prog/dlib/./python_examples/svm_struct.py -> /home/pi/prog/dlib/./dist/dlib/examples/svm_struct.py.
Copying file /home/pi/prog/dlib/./python_examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt -> /home/pi/prog/dlib/./dist/dlib/examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt.
running build_py
copying dist/dlib/__init__.py -> build/lib.linux-armv7l-3.4/dlib
running egg_info
creating dist/dlib.egg-info
writing dependency_links to dist/dlib.egg-info/dependency_links.txt
writing dist/dlib.egg-info/PKG-INFO
writing top-level names to dist/dlib.egg-info/top_level.txt
writing manifest file 'dist/dlib.egg-info/SOURCES.txt'
reading manifest file 'dist/dlib.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
warning: no previously-included files matching '**' found under directory 'dlib/build'
warning: no files found matching '*.bat' under directory 'python_examples'
warning: no previously-included files matching '**' found under directory 'python_examples/build'
writing manifest file 'dist/dlib.egg-info/SOURCES.txt'
copying dist/dlib/dlib.so -> build/lib.linux-armv7l-3.4/dlib
copying dist/dlib/examples/__init__.py -> build/lib.linux-armv7l-3.4/dlib/examples
running build_ext
installing library code to build/bdist.linux-armv7l/egg
running install_lib
creating build/bdist.linux-armv7l/egg
creating build/bdist.linux-armv7l/egg/dlib
copying build/lib.linux-armv7l-3.4/dlib/__init__.py -> build/bdist.linux-armv7l/egg/dlib
creating build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/face_recognition.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/requirements.txt -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/max_cost_assignment.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/find_candidate_object_locations.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/__init__.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/face_detector.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/sequence_segmenter.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/train_shape_predictor.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/correlation_tracker.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/face_landmark_detection.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/train_object_detector.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/svm_rank.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/svm_struct.py -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/examples/LICENSE_FOR_EXAMPLE_PROGRAMS.txt -> build/bdist.linux-armv7l/egg/dlib/examples
copying build/lib.linux-armv7l-3.4/dlib/dlib.so -> build/bdist.linux-armv7l/egg/dlib
byte-compiling build/bdist.linux-armv7l/egg/dlib/__init__.py to __init__.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/face_recognition.py to face_recognition.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/max_cost_assignment.py to max_cost_assignment.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/find_candidate_object_locations.py to find_candidate_object_locations.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/__init__.py to __init__.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/face_detector.py to face_detector.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/sequence_segmenter.py to sequence_segmenter.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/train_shape_predictor.py to train_shape_predictor.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/correlation_tracker.py to correlation_tracker.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/face_landmark_detection.py to face_landmark_detection.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/train_object_detector.py to train_object_detector.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/svm_rank.py to svm_rank.cpython-34.pyc
byte-compiling build/bdist.linux-armv7l/egg/dlib/examples/svm_struct.py to svm_struct.cpython-34.pyc
creating build/bdist.linux-armv7l/egg/EGG-INFO
copying dist/dlib.egg-info/PKG-INFO -> build/bdist.linux-armv7l/egg/EGG-INFO
copying dist/dlib.egg-info/SOURCES.txt -> build/bdist.linux-armv7l/egg/EGG-INFO
copying dist/dlib.egg-info/dependency_links.txt -> build/bdist.linux-armv7l/egg/EGG-INFO
copying dist/dlib.egg-info/not-zip-safe -> build/bdist.linux-armv7l/egg/EGG-INFO
copying dist/dlib.egg-info/top_level.txt -> build/bdist.linux-armv7l/egg/EGG-INFO
writing build/bdist.linux-armv7l/egg/EGG-INFO/native_libs.txt
creating 'dist/dlib-19.4.99-py3.4-linux-armv7l.egg' and adding 'build/bdist.linux-armv7l/egg' to it
removing 'build/bdist.linux-armv7l/egg' (and everything under it)
Processing dlib-19.4.99-py3.4-linux-armv7l.egg
creating /home/pi/.virtualenvs/cv/lib/python3.4/site-packages/dlib-19.4.99-py3.4-linux-armv7l.egg
Extracting dlib-19.4.99-py3.4-linux-armv7l.egg to /home/pi/.virtualenvs/cv/lib/python3.4/site-packages
Adding dlib 19.4.99 to easy-install.pth file

Installed /home/pi/.virtualenvs/cv/lib/python3.4/site-packages/dlib-19.4.99-py3.4-linux-armv7l.egg
Processing dependencies for dlib==19.4.99
Finished processing dependencies for dlib==19.4.99
```
