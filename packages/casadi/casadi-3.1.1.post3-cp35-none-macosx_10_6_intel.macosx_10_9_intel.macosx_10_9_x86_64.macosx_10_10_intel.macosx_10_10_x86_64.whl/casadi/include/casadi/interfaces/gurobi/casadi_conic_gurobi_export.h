
#ifndef CASADI_CONIC_GUROBI_EXPORT_H
#define CASADI_CONIC_GUROBI_EXPORT_H

#ifdef CASADI_CONIC_GUROBI_STATIC_DEFINE
#  define CASADI_CONIC_GUROBI_EXPORT
#  define CASADI_CONIC_GUROBI_NO_EXPORT
#else
#  ifndef CASADI_CONIC_GUROBI_EXPORT
#    ifdef casadi_conic_gurobi_EXPORTS
        /* We are building this library */
#      define CASADI_CONIC_GUROBI_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define CASADI_CONIC_GUROBI_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef CASADI_CONIC_GUROBI_NO_EXPORT
#    define CASADI_CONIC_GUROBI_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef CASADI_CONIC_GUROBI_DEPRECATED
#  define CASADI_CONIC_GUROBI_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef CASADI_CONIC_GUROBI_DEPRECATED_EXPORT
#  define CASADI_CONIC_GUROBI_DEPRECATED_EXPORT CASADI_CONIC_GUROBI_EXPORT CASADI_CONIC_GUROBI_DEPRECATED
#endif

#ifndef CASADI_CONIC_GUROBI_DEPRECATED_NO_EXPORT
#  define CASADI_CONIC_GUROBI_DEPRECATED_NO_EXPORT CASADI_CONIC_GUROBI_NO_EXPORT CASADI_CONIC_GUROBI_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef CASADI_CONIC_GUROBI_NO_DEPRECATED
#    define CASADI_CONIC_GUROBI_NO_DEPRECATED
#  endif
#endif

#endif
