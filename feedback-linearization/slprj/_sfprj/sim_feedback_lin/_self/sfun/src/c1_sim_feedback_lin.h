#ifndef __c1_sim_feedback_lin_h__
#define __c1_sim_feedback_lin_h__

/* Include files */
#include "sf_runtime/sfc_sf.h"
#include "sf_runtime/sfc_mex.h"
#include "rtwtypes.h"
#include "multiword_types.h"

/* Type Definitions */
#ifndef struct_sW0DvJ9G4pdtw8hWPXUfo3G
#define struct_sW0DvJ9G4pdtw8hWPXUfo3G

struct sW0DvJ9G4pdtw8hWPXUfo3G
{
  real_T m1;
  real_T m2;
  real_T l1;
  real_T l2;
  real_T s1;
  real_T s2;
  real_T I1;
  real_T I2;
  real_T b11;
  real_T b22;
  real_T b12;
  real_T b21;
  real_T a1;
  real_T a2;
  real_T a3;
};

#endif                                 /*struct_sW0DvJ9G4pdtw8hWPXUfo3G*/

#ifndef typedef_c1_sW0DvJ9G4pdtw8hWPXUfo3G
#define typedef_c1_sW0DvJ9G4pdtw8hWPXUfo3G

typedef struct sW0DvJ9G4pdtw8hWPXUfo3G c1_sW0DvJ9G4pdtw8hWPXUfo3G;

#endif                                 /*typedef_c1_sW0DvJ9G4pdtw8hWPXUfo3G*/

#ifndef typedef_SFc1_sim_feedback_linInstanceStruct
#define typedef_SFc1_sim_feedback_linInstanceStruct

typedef struct {
  SimStruct *S;
  ChartInfoStruct chartInfo;
  uint32_T chartNumber;
  uint32_T instanceNumber;
  int32_T c1_sfEvent;
  boolean_T c1_isStable;
  boolean_T c1_doneDoubleBufferReInit;
  uint8_T c1_is_active_c1_sim_feedback_lin;
  real_T (*c1_theta)[2];
  real_T (*c1_C)[2];
  real_T (*c1_theta_dot)[2];
} SFc1_sim_feedback_linInstanceStruct;

#endif                                 /*typedef_SFc1_sim_feedback_linInstanceStruct*/

/* Named Constants */

/* Variable Declarations */
extern struct SfDebugInstanceStruct *sfGlobalDebugInstanceStruct;

/* Variable Definitions */

/* Function Declarations */
extern const mxArray *sf_c1_sim_feedback_lin_get_eml_resolved_functions_info
  (void);

/* Function Definitions */
extern void sf_c1_sim_feedback_lin_get_check_sum(mxArray *plhs[]);
extern void c1_sim_feedback_lin_method_dispatcher(SimStruct *S, int_T method,
  void *data);

#endif
