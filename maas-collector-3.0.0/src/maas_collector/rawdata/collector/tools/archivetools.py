"""Extract archive file tgz"""
import os
import tarfile
import zipfile
import fnmatch


def extract_files_in_tar(logger, tar_url, extract_path=".", pattern_file="*") -> list:
    """Extract zip file

    Args:
        logger : collector logger
        tar_url ([str]): archive url
        extract_path ([str]) : extraction file path
        pattern_file ([str]) : pattern to select path
    """
    logger.debug("Extract file %s in %s", tar_url, extract_path)

    extract_files = []

    try:
        # Open tar file
        with tarfile.open(tar_url, "r") as tar_fd:

            # Extract file filtered with pattern file
            for member in tar_fd.getmembers():

                if fnmatch.fnmatch(member.name, pattern_file):
                    tar_fd.extract(member, path=extract_path, set_attrs=False)
                    extract_files.append(os.path.join(extract_path, member.name))

    except tarfile.TarError as err:
        logger.error("Error %s Extract tar file", err)
        raise

    return extract_files


def extract_files_in_zip(logger, zip_url, extract_path=".", pattern_file="*") -> list:
    """Extract zip file

    Args:
        logger : collector logger
        zip_url ([str]): archive url
        extract_path ([str]) : extraction file path
        pattern_file ([str]) : pattern to select path
    """

    logger.debug("Extract file %s in %s", zip_url, extract_path)

    extract_files = []

    try:
        # Open zip file
        with zipfile.ZipFile(zip_url) as zip_fd:
            # Extract file filtered with pattern file
            for member in zip_fd.namelist():

                if fnmatch.fnmatch(member, pattern_file):
                    zip_fd.extract(member, extract_path)
                    extract_files.append(os.path.join(extract_path, member))

    except (zipfile.BadZipfile, IOError) as err:
        logger.error("Error Extract file %s", err)
        raise
    return extract_files
