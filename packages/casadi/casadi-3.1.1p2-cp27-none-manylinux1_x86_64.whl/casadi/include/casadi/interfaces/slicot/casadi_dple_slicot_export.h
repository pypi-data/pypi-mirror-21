
#ifndef CASADI_DPLE_SLICOT_EXPORT_H
#define CASADI_DPLE_SLICOT_EXPORT_H

#ifdef CASADI_DPLE_SLICOT_STATIC_DEFINE
#  define CASADI_DPLE_SLICOT_EXPORT
#  define CASADI_DPLE_SLICOT_NO_EXPORT
#else
#  ifndef CASADI_DPLE_SLICOT_EXPORT
#    ifdef casadi_dple_slicot_EXPORTS
        /* We are building this library */
#      define CASADI_DPLE_SLICOT_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define CASADI_DPLE_SLICOT_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef CASADI_DPLE_SLICOT_NO_EXPORT
#    define CASADI_DPLE_SLICOT_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef CASADI_DPLE_SLICOT_DEPRECATED
#  define CASADI_DPLE_SLICOT_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef CASADI_DPLE_SLICOT_DEPRECATED_EXPORT
#  define CASADI_DPLE_SLICOT_DEPRECATED_EXPORT CASADI_DPLE_SLICOT_EXPORT CASADI_DPLE_SLICOT_DEPRECATED
#endif

#ifndef CASADI_DPLE_SLICOT_DEPRECATED_NO_EXPORT
#  define CASADI_DPLE_SLICOT_DEPRECATED_NO_EXPORT CASADI_DPLE_SLICOT_NO_EXPORT CASADI_DPLE_SLICOT_DEPRECATED
#endif

#define DEFINE_NO_DEPRECATED 0
#if DEFINE_NO_DEPRECATED
# define CASADI_DPLE_SLICOT_NO_DEPRECATED
#endif

#endif
