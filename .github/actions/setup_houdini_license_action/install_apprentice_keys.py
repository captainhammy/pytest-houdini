"""This script is used to get and install non-commercial Houdini licenses."""

# Future
from __future__ import annotations

# Standard Library
import argparse
import socket
import subprocess
from typing import List

# SideFX
import sidefx

ACCESS_TOKEN_URL = "https://www.sidefx.com/oauth2/application_token"
ENDPOINT_URL = "https://www.sidefx.com/api/"
PRODUCTS_TO_INSTALL = "HOUDINI-NC;RENDER-NC"


def build_parser() -> argparse.ArgumentParser:
    """Build an argument parser to get the command line data.

    Returns:
        An argument parser to get the required input information.

    """
    parser = argparse.ArgumentParser()

    parser.add_argument("client_id")

    parser.add_argument("client_secret")

    parser.add_argument("houdini_version")

    return parser


def get_keys_to_install(
    client_id: str,
    client_secret_key: str,
    houdini_version: str,
    server_name: str,
    server_code: str,
) -> List[str]:
    """Get a list of non-commercial license keys to install.

    Args:
        client_id: The SideFX client id.
        client_secret_key: The SideFX client secret.
        houdini_version: The Houdini version to request a license for.
        server_name: The local server name.
        server_code: The local server code.

    Returns:
        The list of license keys to install.
    """
    service = sidefx.service(
        access_token_url=ACCESS_TOKEN_URL,
        client_id=client_id,
        client_secret_key=client_secret_key,
        endpoint_url=ENDPOINT_URL,
    )

    license_strings = service.license.get_non_commercial_license(
        server_name=server_name,
        server_code=server_code,
        version=houdini_version,
        products=PRODUCTS_TO_INSTALL,
    )
    return license_strings["license_keys"]


def get_server_code() -> str:
    """Get the server code for the locally running server.

    Returns:
        The sesinetd server code.
    """
    result = subprocess.check_output(["sesictrl", "print-server"])
    server_code = result.decode().split("\n")[1].split()[2]

    return server_code


def install_licenses(license_keys: List[str]) -> None:
    """Install a list of license keys.

    Args:
        license_keys: The licenses keys to install.
    """
    for license_key in license_keys:
        subprocess.call(["sesictrl", "install", license_key])


def main() -> None:
    """The main execution function."""
    # Parse the args from the action execution.
    parser = build_parser()
    parsed_args = parser.parse_args()

    server_code = get_server_code()
    server_name = socket.getfqdn()

    license_keys = get_keys_to_install(
        parsed_args.client_id,
        parsed_args.client_secret,
        parsed_args.houdini_version,
        server_name,
        server_code,
    )

    install_licenses(license_keys)


if __name__ == "__main__":
    main()
