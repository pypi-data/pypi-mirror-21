def configuration(parent_package='', top_path=None):
    import os
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils import fcompiler

    # figure out which compiler we're going to use
    compiler = fcompiler.get_default_fcompiler()
    # set some fortran compiler-dependent flags (following CliMT code here)
    if compiler == 'gnu95':
        #f77flags=['-ffixed-line-length-132', '-fdefault-real-8']
        #f90flags='-fdefault-real-8 -fno-range-check -ffree-form'
        f90flags=['-fdefault-real-8']
    elif compiler == 'intel' or compiler == 'intelem':
        #f77flags='-132 -r8'
        f90flags=['-132', '-r8']
    print f90flags

    here = os.path.abspath(os.path.dirname(__file__))
    sourcelistfile = os.path.join(here, 'sources_in_order_of_compilation')
    sourcelist = [line.rstrip() for line in open(sourcelistfile)]
    sourcelist.append('_cam3.pyf')

    config = Configuration(package_name='cam3', parent_name=parent_package, top_path=top_path)
    config.add_extension(name='_cam3',
                         sources=sourcelist,
                         extra_f90_compile_args=f90flags)                         
    config.add_include_dirs('src')
    config.add_data_files(os.path.join('data', 'abs_ems_factors_fastvx.c030508.nc'))
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
