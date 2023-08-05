import os
import re
import subprocess
import tempfile

from vdist.builder import Builder
from vdist.source import git, git_directory, directory

DEB_COMPILE_FILTER = [r'[^\.]', r'\./$', r'\./usr/', r'\./opt/$']
DEB_NOCOMPILE_FILTER = [r'[^\.]', r'^\.\.', r'\./$', r'^\.$', r'\./opt/$']

FPM_ARGS = '--maintainer dante.signal31@gmail.com -a native --url ' \
           'https://github.com/dante-signal31/geolocate --description ' \
           '"This program accepts any text and searchs inside every IP' \
           ' address. With each of those IP addresses, ' \
           'geolocate queries ' \
           'Maxmind GeoIP database to look for the city and ' \
           'country where' \
           ' IP address or URL is located. Geolocate is designed to be' \
           ' used in console with pipes and redirections along with ' \
           'applications like traceroute, nslookup, etc.' \
           ' " --license BSD-3 --category net '


def _read_deb_contents(deb_file_pathname):
    entries = os.popen("dpkg -c {0}".format(deb_file_pathname)).readlines()
    file_list = [entry.split()[-1] for entry in entries]
    return file_list


def _read_rpm_contents(rpm_file_pathname):
    entries = os.popen("rpm -qlp {0}".format(rpm_file_pathname)).readlines()
    file_list = [entry.rstrip("\n") for entry in entries
                 if entry.startswith("/")]
    return file_list


def _purge_list(original_list, purgables):
    list_purged = []
    for entry in original_list:
        entry_free_of_purgables = all(True if re.match(pattern, entry) is None
                                      else False
                                      for pattern in purgables)
        if entry_free_of_purgables:
            list_purged.append(entry)
    return list_purged


def _call_builder(builder_parameters):
    builder = Builder()
    builder.add_build(**builder_parameters)
    builder.build()


def _generate_rpm(builder_parameters, centos_version):
    _call_builder(builder_parameters)
    homedir = os.path.expanduser('~')
    filename_prefix = "-".join([builder_parameters["app"],
                                builder_parameters["version"]])
    target_file = os.path.join(
        homedir,
        '.vdist',
        'dist',
        "".join([filename_prefix, "-{0}".format(centos_version)]),
        "".join([filename_prefix, '-1.x86_64.rpm']),
    )
    assert os.path.isfile(target_file)
    assert os.path.getsize(target_file) > 0
    return target_file


def _generate_deb(builder_parameters):
    _call_builder(builder_parameters)
    homedir = os.path.expanduser('~')
    filename_prefix = "-".join([builder_parameters["app"],
                                builder_parameters["version"]])
    deb_filename_prefix = "_".join([builder_parameters["app"],
                                    builder_parameters["version"]])
    target_file = os.path.join(
        homedir,
        '.vdist',
        'dist',
        "".join([filename_prefix, "-ubuntu-trusty"]),
        "".join([deb_filename_prefix, '_amd64.deb']),
    )
    assert os.path.isfile(target_file)
    assert os.path.getsize(target_file) > 0
    return target_file


def _get_purged_deb_file_list(deb_filepath, file_filter):
    file_list = _read_deb_contents(deb_filepath)
    file_list_purged = _purge_list(file_list, file_filter)
    return file_list_purged


def test_generate_deb_from_git():
    builder_parameters = {"app": 'vdist-test-generate-deb-from-git',
                          "version": '1.0',
                          "source": git(
                              uri='https://github.com/objectified/vdist',
                              branch='master'
                          ),
                          "profile": 'ubuntu-trusty'}
    _ = _generate_deb(builder_parameters)


def _generate_rpm_from_git(centos_version):
    builder_parameters = {"app": 'vdist-test-generate-rpm-from-git',
                          "version": '1.0',
                          "source": git(
                              uri='https://github.com/objectified/vdist',
                              branch='master'
                          ),
                          "profile": centos_version}
    _ = _generate_rpm(builder_parameters, centos_version)


def test_generate_rpm_from_git_centos6():
    _generate_rpm_from_git("centos6")


def test_generate_rpm_from_git_centos7():
    _generate_rpm_from_git("centos7")


# Scenarios to test:
# 1.- Project containing a setup.py and compiles Python -> only package the
#     whole Python basedir.
# 2.- Project not containing a setup.py and compiles Python -> package both the
#     project dir and the Python basedir.
# 3.- Project containing a setup.py and using a prebuilt Python package (e.g.
#     not compiling) -> package the custom Python basedir only
# 4.- Project not containing a setup.py and using a prebuilt Python package ->
#     package both the project dir and the Python basedir
# More info at:
#   https://github.com/objectified/vdist/pull/7#issuecomment-177818848


# Scenario 1 - Project containing a setup.py and compiles Python -> only package
# the whole Python basedir.
def test_generate_deb_from_git_setup_compile():
    builder_parameters = {
        "app": 'geolocate',
        "version": '1.3.0',
        "source": git(
            uri='https://github.com/dante-signal31/geolocate',
            branch='master'
        ),
        "profile": 'ubuntu-trusty',
        "compile_python": True,
        "python_version": '3.4.4',
        "fpm_args": FPM_ARGS,
        "requirements_path": '/REQUIREMENTS.txt',
        "runtime_deps": ["libssl1.0.0", ],
        "after_install": 'packaging/postinst.sh',
        "after_remove": 'packaging/postuninst.sh'
    }
    target_file = _generate_deb(builder_parameters)
    file_list_purged = _get_purged_deb_file_list(target_file,
                                                 DEB_COMPILE_FILTER)
    # At this point only a folder should remain if everything is correct.
    correct_install_path = "./opt/geolocate"
    assert all((True if correct_install_path in file_entry else False
                for file_entry in file_list_purged))
    # Geolocate launcher should be in bin folder too.
    geolocate_launcher = "./opt/geolocate/bin/geolocate"
    assert geolocate_launcher in file_list_purged


def _generate_rpm_from_git_setup_compile(centos_version):
    builder_parameters = {
        "app": 'geolocate',
        "version": '1.3.0',
        "source": git(
            uri='https://github.com/dante-signal31/geolocate',
            branch='master'
        ),
        "profile": centos_version,
        "compile_python": True,
        "python_version": '3.4.4',
        "fpm_args": FPM_ARGS,
        "requirements_path": '/REQUIREMENTS.txt',
        "runtime_deps": ["libssl1.0.0", ],
        "after_install": 'packaging/postinst.sh',
        "after_remove": 'packaging/postuninst.sh'
    }
    target_file = _generate_rpm(builder_parameters, centos_version)
    file_list = _read_rpm_contents(target_file)
    # At this point only a folder should remain if everything is correct.
    correct_install_path = "/opt/geolocate"
    assert all((True if correct_install_path in file_entry else False
                for file_entry in file_list))
    # Geolocate launcher should be in bin folder too.
    geolocate_launcher = "/opt/geolocate/bin/geolocate"
    assert geolocate_launcher in file_list


def test_generate_rpm_from_git_setup_compile_centos6():
    _generate_rpm_from_git_setup_compile("centos6")


def test_generate_rpm_from_git_setup_compile_centos7():
    _generate_rpm_from_git_setup_compile("centos7")


# Scenario 2.- Project not containing a setup.py and compiles Python -> package
# both the project dir and the Python basedir
def test_generate_deb_from_git_nosetup_compile():
    builder_parameters = {"app": 'jtrouble',
                          "version": '1.0.0',
                          "source": git(
                                uri='https://github.com/objectified/jtrouble',
                                branch='master'
                          ),
                          "profile": 'ubuntu-trusty',
                          "package_install_root": "/opt",
                          "python_basedir": "/opt/python",
                          "compile_python": True,
                          "python_version": '3.4.4', }
    target_file = _generate_deb(builder_parameters)
    file_list_purged = _get_purged_deb_file_list(target_file,
                                                 DEB_COMPILE_FILTER)
    # At this point only two folders should remain if everything is correct:
    # application folder and compiled interpreter folder.
    correct_folders = ["./opt/jtrouble", "./opt/python"]
    assert all((True if any(folder in file_entry for folder in correct_folders)
                else False
                for file_entry in file_list_purged))
    assert any(correct_folders[0] in file_entry
               for file_entry in file_list_purged)
    assert any(correct_folders[1] in file_entry
               for file_entry in file_list_purged)


def _generate_rpm_from_git_nosetup_compile(centos_version):
    builder_parameters = {"app": 'jtrouble',
                          "version": '1.0.0',
                          "source": git(
                                uri='https://github.com/objectified/jtrouble',
                                branch='master'
                          ),
                          "profile": centos_version,
                          "package_install_root": "/opt",
                          "python_basedir": "/opt/python",
                          "compile_python": True,
                          "python_version": '3.4.4', }
    target_file = _generate_rpm(builder_parameters, centos_version)
    file_list = _read_rpm_contents(target_file)
    # At this point only two folders should remain if everything is correct:
    # application folder and compiled interpreter folder.
    correct_folders = ["/opt/jtrouble", "/opt/python"]
    assert all((True if any(folder in file_entry for folder in correct_folders)
                else False
                for file_entry in file_list))
    assert any(correct_folders[0] in file_entry
               for file_entry in file_list)
    assert any(correct_folders[1] in file_entry
               for file_entry in file_list)


def test_generate_rpm_from_git_nosetup_compile_centos6():
    _generate_rpm_from_git_nosetup_compile("centos6")


def test_generate_rpm_from_git_nosetup_compile_centos7():
    _generate_rpm_from_git_nosetup_compile("centos7")


# Scenario 3 - Project containing a setup.py and using a prebuilt Python package
# (e.g. not compiling) -> package the custom Python basedir only.
def test_generate_deb_from_git_setup_nocompile():
    builder_parameters = {
        "app": 'geolocate',
        "version": '1.3.0',
        "source": git(
            uri='https://github.com/dante-signal31/geolocate',
            branch='master'
        ),
        "profile": 'ubuntu-trusty',
        "compile_python": False,
        "python_version": '3.4.4',
        # Lets suppose custom python package is already installed and its root
        # folder is /usr. Actually I'm using default installed python3
        # package, it's is going to be a huge package but this way don't
        # need a private package repository.
        "python_basedir": '/usr',
        "fpm_args": FPM_ARGS,
        "requirements_path": '/REQUIREMENTS.txt',
        "runtime_deps": ["libssl1.0.0", ],
        "after_install": 'packaging/postinst.sh',
        "after_remove": 'packaging/postuninst.sh'
    }
    target_file = _generate_deb(builder_parameters)
    file_list_purged = _get_purged_deb_file_list(target_file,
                                                 DEB_NOCOMPILE_FILTER)
    # At this point only a folder should remain if everything is correct.
    correct_install_path = "./usr"
    assert all((True if correct_install_path in file_entry else False
                for file_entry in file_list_purged))
    # If python basedir was properly packaged then /usr/bin/python should be
    # there.
    python_interpreter = "./usr/bin/python2.7"
    assert python_interpreter in file_list_purged
    # If application was properly packaged then launcher should be in bin folder
    # too.
    geolocate_launcher = "./usr/local/bin/geolocate"
    assert geolocate_launcher in file_list_purged


def _generate_rpm_from_git_setup_nocompile(centos_version):
    builder_parameters = {
        "app": 'geolocate',
        "version": '1.3.0',
        "source": git(
            uri='https://github.com/dante-signal31/geolocate',
            branch='master'
        ),
        "profile": centos_version,
        "compile_python": False,
        "python_version": '3.4.4',
        # Lets suppose custom python package is already installed and its root
        # folder is /usr. Actually I'm using default installed python3
        # package, it's is going to be a huge package but this way don't
        # need a private package repository.
        "python_basedir": '/usr',
        "fpm_args": FPM_ARGS,
        "requirements_path": '/REQUIREMENTS.txt',
        "runtime_deps": ["libssl1.0.0", ],
        "after_install": 'packaging/postinst.sh',
        "after_remove": 'packaging/postuninst.sh'
    }
    target_file = _generate_rpm(builder_parameters, centos_version)
    file_list = _read_rpm_contents(target_file)
    # At this point only a folder should remain if everything is correct.
    correct_install_path = "/usr"
    assert all((True if correct_install_path in file_entry else False
                for file_entry in file_list))
    # If python basedir was properly packaged then /usr/bin/python should be
    # there.
    python_interpreter = "/usr/bin/python"
    assert python_interpreter in file_list
    # If application was properly packaged then launcher should be in bin folder
    # too.
    geolocate_launcher = "/usr/bin/geolocate"
    assert geolocate_launcher in file_list


def test_generate_rpm_from_git_setup_nocompile_centos6():
    _generate_rpm_from_git_setup_nocompile("centos6")


# TODO: This test fails <<<<<<<<<<<<<
# WARNING: Something wrong happens with "nocompile" tests in centos7.
# I don't know why fpm call corrupts some lib in the linux container so
# further cp command fails. This does not happen in centos6 or debian even
# when fpm commands are the same. Any help with this issue will be welcome.
def test_generate_rpm_from_git_setup_nocompile_centos7():
    _generate_rpm_from_git_setup_nocompile("centos7")


# Scenario 4.- Project not containing a setup.py and using a prebuilt Python
# package -> package both the project dir and the Python basedir
def test_generate_deb_from_git_nosetup_nocompile():
    builder_parameters = {
        "app": 'jtrouble',
        "version": '1.0.0',
        "source": git(
            uri='https://github.com/objectified/jtrouble',
            branch='master'
        ),
        "profile": 'ubuntu-trusty',
        "compile_python": False,
        # Here happens the same than in
        # test_generate_deb_from_git_setup_nocompile()
        "python_version": '3.4.4',
        "python_basedir": '/usr',
    }
    target_file = _generate_deb(builder_parameters)
    file_list_purged = _get_purged_deb_file_list(target_file,
                                                 DEB_NOCOMPILE_FILTER)
    # At this point only two folders should remain if everything is correct:
    # application folder and python basedir folder.
    correct_folders = ["./opt/jtrouble", "./usr"]
    assert all((True if any(folder in file_entry for folder in correct_folders)
                else False
                for file_entry in file_list_purged))
    # If python basedir was properly packaged then /usr/bin/python should be
    # there.
    python_interpreter = "./usr/bin/python2.7"
    assert python_interpreter in file_list_purged


def _generate_rpm_from_git_nosetup_nocompile(centos_version):
    builder_parameters = {
        "app": 'jtrouble',
        "version": '1.0.0',
        "source": git(
            uri='https://github.com/objectified/jtrouble',
            branch='master'
        ),
        "profile": centos_version,
        "compile_python": False,
        # Here happens the same than in
        # test_generate_deb_from_git_setup_nocompile()
        "python_version": '3.4.4',
        "python_basedir": '/usr',
    }
    target_file = _generate_rpm(builder_parameters, centos_version)
    file_list = _read_rpm_contents(target_file)
    # At this point only two folders should remain if everything is correct:
    # application folder and python basedir folder.
    correct_folders = ["/opt/jtrouble", "/usr"]
    assert all((True if any(folder in file_entry for folder in correct_folders)
                else False
                for file_entry in file_list))
    # If python basedir was properly packaged then /usr/bin/python should be
    # there.
    python_interpreter = "/usr/bin/python"
    assert python_interpreter in file_list


def test_generate_rpm_from_git_nosetup_nocompile_centos6():
    _generate_rpm_from_git_nosetup_nocompile("centos6")


# TODO: This test fails <<<<<<<<<<<<<
# WARNING: Something wrong happens with "nocompile" tests in centos7.
# I don't know why fpm call corrupts some lib in the linux container so
# further cp command fails. This does not happen in centos6 or debian even
# when fpm commands are the same. Any help with this issue will be welcome.
def test_generate_rpm_from_git_nosetup_nocompile_centos7():
    _generate_rpm_from_git_nosetup_nocompile("centos7")


def test_generate_deb_from_git_suffixed():
    builder_parameters = {"app": 'vdist-test-generate-deb-from-git-suffixed',
                          "version": '1.0',
                          "source": git(
                            uri='https://github.com/objectified/vdist.git',
                            branch='master'
                          ),
                          "profile": 'ubuntu-trusty'}
    _ = _generate_deb(builder_parameters)


def _generate_rpm_from_git_suffixed(centos_version):
    builder_parameters = {"app": 'vdist-test-generate-deb-from-git-suffixed',
                          "version": '1.0',
                          "source": git(
                            uri='https://github.com/objectified/vdist.git',
                            branch='master'
                          ),
                          "profile": centos_version}
    _ = _generate_rpm(builder_parameters, centos_version)


def test_generate_rpm_from_git_suffixed_centos6():
    _generate_rpm_from_git_suffixed("centos6")


def test_generate_rpm_from_git_suffixed_centos7():
    _generate_rpm_from_git_suffixed("centos7")


def test_generate_deb_from_git_directory():
    tempdir = tempfile.gettempdir()
    checkout_dir = os.path.join(tempdir, 'vdist')

    git_p = subprocess.Popen(
        ['git', 'clone',
         'https://github.com/objectified/vdist',
         checkout_dir])
    git_p.communicate()

    builder_parameters = {"app": 'vdist-test-generate-deb-from-git-dir',
                          "version": '1.0',
                          "source": git_directory(path=checkout_dir,
                                                  branch='master'),
                          "profile": 'ubuntu-trusty'}
    _ = _generate_deb(builder_parameters)


def _generate_rpm_from_git_directory(centos_version):
    tempdir = tempfile.gettempdir()
    checkout_dir = os.path.join(tempdir, 'vdist')

    git_p = subprocess.Popen(
        ['git', 'clone',
         'https://github.com/objectified/vdist',
         checkout_dir])
    git_p.communicate()

    builder_parameters = {"app": 'vdist-test-generate-deb-from-git-dir',
                          "version": '1.0',
                          "source": git_directory(path=checkout_dir,
                                                  branch='master'),
                          "profile": centos_version}
    _ = _generate_rpm(builder_parameters, centos_version)


def test_generate_rpm_from_git_directory_centos6():
    _generate_rpm_from_git_directory("centos6")


def test_generate_rpm_from_git_directory_centos7():
    _generate_rpm_from_git_directory("centos7")


def test_generate_deb_from_directory():
    tempdir = tempfile.gettempdir()
    checkout_dir = os.path.join(tempdir, 'vdist')

    git_p = subprocess.Popen(
        ['git', 'clone',
         'https://github.com/objectified/vdist',
         checkout_dir])
    git_p.communicate()

    builder_parameters = {"app": 'vdist-test-generate-deb-from-dir',
                          "version": '1.0',
                          "source": directory(path=checkout_dir, ),
                          "profile": 'ubuntu-trusty'}
    _ = _generate_deb(builder_parameters)


def _generate_rpm_from_directory(centos_version):
    tempdir = tempfile.gettempdir()
    checkout_dir = os.path.join(tempdir, 'vdist')

    git_p = subprocess.Popen(
        ['git', 'clone',
         'https://github.com/objectified/vdist',
         checkout_dir])
    git_p.communicate()

    builder_parameters = {"app": 'vdist-test-generate-deb-from-dir',
                          "version": '1.0',
                          "source": directory(path=checkout_dir, ),
                          "profile": centos_version}
    _ = _generate_rpm(builder_parameters, centos_version)


def test_generate_rpm_from_directory_centos6():
    _generate_rpm_from_directory("centos6")


def test_generate_rpm_from_directory_centos7():
    _generate_rpm_from_directory("centos7")

