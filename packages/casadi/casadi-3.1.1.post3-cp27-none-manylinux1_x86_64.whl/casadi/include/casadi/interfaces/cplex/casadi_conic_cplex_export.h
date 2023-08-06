
#ifndef CASADI_CONIC_CPLEX_EXPORT_H
#define CASADI_CONIC_CPLEX_EXPORT_H

#ifdef CASADI_CONIC_CPLEX_STATIC_DEFINE
#  define CASADI_CONIC_CPLEX_EXPORT
#  define CASADI_CONIC_CPLEX_NO_EXPORT
#else
#  ifndef CASADI_CONIC_CPLEX_EXPORT
#    ifdef casadi_conic_cplex_EXPORTS
        /* We are building this library */
#      define CASADI_CONIC_CPLEX_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define CASADI_CONIC_CPLEX_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef CASADI_CONIC_CPLEX_NO_EXPORT
#    define CASADI_CONIC_CPLEX_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef CASADI_CONIC_CPLEX_DEPRECATED
#  define CASADI_CONIC_CPLEX_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef CASADI_CONIC_CPLEX_DEPRECATED_EXPORT
#  define CASADI_CONIC_CPLEX_DEPRECATED_EXPORT CASADI_CONIC_CPLEX_EXPORT CASADI_CONIC_CPLEX_DEPRECATED
#endif

#ifndef CASADI_CONIC_CPLEX_DEPRECATED_NO_EXPORT
#  define CASADI_CONIC_CPLEX_DEPRECATED_NO_EXPORT CASADI_CONIC_CPLEX_NO_EXPORT CASADI_CONIC_CPLEX_DEPRECATED
#endif

#define DEFINE_NO_DEPRECATED 0
#if DEFINE_NO_DEPRECATED
# define CASADI_CONIC_CPLEX_NO_DEPRECATED
#endif

#endif
