
#ifndef CASADI_NLPSOL_SNOPT_EXPORT_H
#define CASADI_NLPSOL_SNOPT_EXPORT_H

#ifdef CASADI_NLPSOL_SNOPT_STATIC_DEFINE
#  define CASADI_NLPSOL_SNOPT_EXPORT
#  define CASADI_NLPSOL_SNOPT_NO_EXPORT
#else
#  ifndef CASADI_NLPSOL_SNOPT_EXPORT
#    ifdef casadi_nlpsol_snopt_EXPORTS
        /* We are building this library */
#      define CASADI_NLPSOL_SNOPT_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define CASADI_NLPSOL_SNOPT_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef CASADI_NLPSOL_SNOPT_NO_EXPORT
#    define CASADI_NLPSOL_SNOPT_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef CASADI_NLPSOL_SNOPT_DEPRECATED
#  define CASADI_NLPSOL_SNOPT_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef CASADI_NLPSOL_SNOPT_DEPRECATED_EXPORT
#  define CASADI_NLPSOL_SNOPT_DEPRECATED_EXPORT CASADI_NLPSOL_SNOPT_EXPORT CASADI_NLPSOL_SNOPT_DEPRECATED
#endif

#ifndef CASADI_NLPSOL_SNOPT_DEPRECATED_NO_EXPORT
#  define CASADI_NLPSOL_SNOPT_DEPRECATED_NO_EXPORT CASADI_NLPSOL_SNOPT_NO_EXPORT CASADI_NLPSOL_SNOPT_DEPRECATED
#endif

#define DEFINE_NO_DEPRECATED 0
#if DEFINE_NO_DEPRECATED
# define CASADI_NLPSOL_SNOPT_NO_DEPRECATED
#endif

#endif
