# ------------------- Required for MSVC nmake ---------------------------------
# This file should be included at the top of a MAKEFILE as follows:


CPU = AMD64

MACHINE     = sim_feedback_lin
TARGET      = sfun
CHART_SRCS   = c1_sim_feedback_lin.c
MACHINE_SRC  = sim_feedback_lin_sfun.c
MACHINE_REG = sim_feedback_lin_sfun_registry.c
MAKEFILE    = sim_feedback_lin_sfun.mak
MATLAB_ROOT  = C:\Program Files\MATLAB\MATLAB Production Server\R2015a
BUILDARGS   =

#--------------------------- Tool Specifications ------------------------------
#
#
MSVC_ROOT1 = $(MSDEVDIR:SharedIDE=vc)
MSVC_ROOT2 = $(MSVC_ROOT1:SHAREDIDE=vc)
MSVC_ROOT  = $(MSVC_ROOT2:sharedide=vc)

# Compiler tool locations, CC, LD, LIBCMD:
CC     = cl.exe
LD     = link.exe
LIBCMD = lib.exe
#------------------------------ Include/Lib Path ------------------------------

USER_INCLUDES   = 
AUX_INCLUDES   = 
MLSLSF_INCLUDES = \
    /I "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\include" \
    /I "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\simulink\include" \
    /I "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\stateflow\c\mex\include" \
    /I "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\rtw\c\src" \
    /I "C:\Users\Ian\Documents\School\Thesis\Optimal Motor Control\Feedback Linearization Test\slprj\_sfprj\sim_feedback_lin\_self\sfun\src" 

COMPILER_INCLUDES = /I "$(MSVC_ROOT)\include"

THIRD_PARTY_INCLUDES   = 
INCLUDE_PATH = $(USER_INCLUDES) $(AUX_INCLUDES) $(MLSLSF_INCLUDES)\
 $(THIRD_PARTY_INCLUDES)
LIB_PATH     = "$(MSVC_ROOT)\lib"

CFLAGS = /c /Zp8 /GR /W3 /EHs /D_CRT_SECURE_NO_DEPRECATE /D_SCL_SECURE_NO_DEPRECATE /D_SECURE_SCL=0 /DMATLAB_MEX_FILE /nologo /MD 
LDFLAGS = /nologo /dll /MANIFEST /OPT:NOREF /export:mexFunction  
#----------------------------- Source Files -----------------------------------

REQ_SRCS  =  $(MACHINE_SRC) $(MACHINE_REG) $(CHART_SRCS)

USER_ABS_OBJS =

AUX_ABS_OBJS =

THIRD_PARTY_OBJS =

REQ_OBJS = $(REQ_SRCS:.cpp=.obj)
REQ_OBJS2 = $(REQ_OBJS:.c=.obj)
OBJS = $(REQ_OBJS2) $(USER_ABS_OBJS) $(AUX_ABS_OBJS) $(THIRD_PARTY_OBJS)
OBJLIST_FILE = sim_feedback_lin_sfun.mol
SFCLIB = 
AUX_LNK_OBJS =     
USER_LIBS = 
LINK_MACHINE_LIBS = 
BLAS_LIBS = "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libmwblas.lib" 
THIRD_PARTY_LIBS = 

#--------------------------------- Rules --------------------------------------

MEX_FILE_NAME_WO_EXT = $(MACHINE)_$(TARGET)
MEX_FILE_NAME = $(MEX_FILE_NAME_WO_EXT).mexw64
MEX_FILE_CSF =
all : $(MEX_FILE_NAME) $(MEX_FILE_CSF)

TMWLIB = "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\sf_runtime.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libmx.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libmex.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libmat.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libfixedpoint.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libut.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libmwmathutil.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libemlrt.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libmwsl_log_load_blocks.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\extern\lib\win64\microsoft\libmwsimulink.lib" "C:\Program Files\MATLAB\MATLAB Production Server\R2015a\lib\win64\libmwipp.lib" 

$(MEX_FILE_NAME) : $(MAKEFILE) $(OBJS) $(SFCLIB) $(AUX_LNK_OBJS) $(USER_LIBS) $(THIRD_PARTY_LIBS)
 @echo ### Linking ...
 $(LD) $(LDFLAGS) /OUT:$(MEX_FILE_NAME) /map:"$(MEX_FILE_NAME_WO_EXT).map"\
  $(USER_LIBS) $(SFCLIB) $(AUX_LNK_OBJS)\
  $(TMWLIB) $(LINK_MACHINE_LIBS) $(DSP_LIBS) $(BLAS_LIBS) $(THIRD_PARTY_LIBS)\
  @$(OBJLIST_FILE)
     mt -outputresource:"$(MEX_FILE_NAME);2" -manifest "$(MEX_FILE_NAME).manifest"
	@echo ### Created $@

.c.obj :
	@echo ### Compiling "$<"
	$(CC) $(CFLAGS) $(INCLUDE_PATH) "$<"

.cpp.obj :
	@echo ### Compiling "$<"
	$(CC) $(CFLAGS) $(INCLUDE_PATH) "$<"


