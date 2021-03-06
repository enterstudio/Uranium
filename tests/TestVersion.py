# Copyright (c) 2018 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

from UM.Version import Version
from unittest import TestCase
import pytest

major_versions = [Version("1"), Version(b"1"), Version(1), Version([1]), Version(["1"]), Version("1."), Version("MOD-1"), Version("1B")]
major_minor_versions = [Version("1.2"), Version("1-2"), Version("1_2"), Version(b"1.2"), Version("1.2BETA"), Version([1, 2]), Version(["1", "2"]), Version([1, "2"]), Version([1, b"2"])]
major_minor_revision_versions = [Version("1.2.3"), Version("1.2.3BETA"), Version("1_2-3"), Version(b"1.2.3"), Version([1, 2, 3]), Version(["1", "2", "3"]), Version([1, "2", 3]), Version("MOD-1.2.3"), Version(["1", 2, b"3"])]


def check_version_equals(first_version: Version, second_version: Version):
    assert first_version == second_version
    assert first_version.getMajor() == second_version.getMajor()
    assert first_version.getMinor() == second_version.getMinor()
    assert first_version.getRevision() == second_version.getRevision()


@pytest.mark.parametrize("first_version", major_versions)
@pytest.mark.parametrize("second_version", major_versions)
def test_major_equals(first_version, second_version):
    check_version_equals(first_version, second_version)


@pytest.mark.parametrize("first_version", major_minor_versions)
@pytest.mark.parametrize("second_version", major_minor_versions)
def test_major_and_minor_equals(first_version, second_version):
    check_version_equals(first_version, second_version)


@pytest.mark.parametrize("first_version", major_minor_revision_versions)
@pytest.mark.parametrize("second_version", major_minor_revision_versions)
def test_major_minor_revision_equals(first_version, second_version):
    check_version_equals(first_version, second_version)


@pytest.mark.parametrize("first_version", major_versions)
@pytest.mark.parametrize("second_version", major_minor_versions)
def test_check_version_smaller(first_version, second_version):
    assert first_version < second_version

    # Just to be on the really safe side
    assert first_version != second_version
    assert not first_version > second_version


@pytest.mark.parametrize("first_version", major_minor_versions)
@pytest.mark.parametrize("second_version", major_minor_revision_versions)
def test_check_version_smaller_2(first_version, second_version):
    assert first_version < second_version

    # Just to be on the really safe side
    assert first_version != second_version
    assert not first_version > second_version
