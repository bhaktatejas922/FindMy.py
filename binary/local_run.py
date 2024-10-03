# ruff: noqa: ASYNC230

import json
from pathlib import Path

from findmy.reports import (
    AppleAccount,
    AsyncAppleAccount,
    BaseAnisetteProvider,
    LoginState,
    SmsSecondFactorMethod,
    TrustedDeviceSecondFactorMethod,
)
import argparse
import json
import requests
from findmy.reports import RemoteAnisetteProvider

ANISETTE_SERVER = "http://192.184.250.198:6969"
# API_ENDPOINT = "http://localhost:8000/register_icloud"
API_ENDPOINT = "https://api.airpinpoint.com/register_icloud"


def _login_sync(account: AppleAccount) -> None:
    email = input("email?  > ")
    password = input("passwd? > ")

    state = account.login(email, password)

    if state == LoginState.REQUIRE_2FA:  # Account requires 2FA
        # This only supports SMS methods for now
        methods = account.get_2fa_methods()

        # Print the (masked) phone numbers
        for i, method in enumerate(methods):
            if isinstance(method, TrustedDeviceSecondFactorMethod):
                print(f"{i} - Trusted Device")
            elif isinstance(method, SmsSecondFactorMethod):
                print(f"{i} - SMS ({method.phone_number})")

        ind = int(input("Method? > "))

        method = methods[ind]
        method.request()
        code = input("Code? > ")

        # This automatically finishes the post-2FA login flow
        method.submit(code)


async def _login_async(account: AsyncAppleAccount) -> None:
    email = input("email?  > ")
    password = input("passwd? > ")

    state = await account.login(email, password)

    if state == LoginState.REQUIRE_2FA:  # Account requires 2FA
        # This only supports SMS methods for now
        methods = await account.get_2fa_methods()

        # Print the (masked) phone numbers
        for i, method in enumerate(methods):
            if isinstance(method, TrustedDeviceSecondFactorMethod):
                print(f"{i} - Trusted Device")
            elif isinstance(method, SmsSecondFactorMethod):
                print(f"{i} - SMS ({method.phone_number})")

        ind = int(input("Method? > "))

        method = methods[ind]
        await method.request()
        code = input("Code? > ")

        # This automatically finishes the post-2FA login flow
        await method.submit(code)


def get_account_sync(anisette: BaseAnisetteProvider) -> AppleAccount:
    """Tries to restore a saved Apple account, or prompts the user for login otherwise. (sync)"""
    acc = AppleAccount(anisette)

    # Save / restore account logic
    acc_store = Path("account.json")
    try:
        with acc_store.open() as f:
            acc.restore(json.load(f))
    except FileNotFoundError:
        _login_sync(acc)
        with acc_store.open("w+") as f:
            json.dump(acc.export(), f)

    return acc


async def get_account_async(anisette: BaseAnisetteProvider) -> AsyncAppleAccount:
    """Tries to restore a saved Apple account, or prompts the user for login otherwise. (async)"""
    acc = AsyncAppleAccount(anisette)

    # Save / restore account logic
    acc_store = Path("account.json")
    try:
        with acc_store.open() as f:
            acc.restore(json.load(f))
    except FileNotFoundError:
        await _login_async(acc)
        with acc_store.open("w+") as f:
            json.dump(acc.export(), f)

    return acc

def get_account_sync_in_memory(anisette: BaseAnisetteProvider) -> dict:
    """Creates an Apple account in memory without saving to a file, and returns the account data as a dict."""
    acc = AppleAccount(anisette)

    _login_sync(acc)
    
    # Export the account data to a dict instead of saving to a file
    account_data = acc.export()
    
    return account_data



def register_icloud(api_key):
    print("Logging into iCloud account")
    anisette = RemoteAnisetteProvider(ANISETTE_SERVER)
    account_data = get_account_sync_in_memory(anisette)

    print("Sending account data to AirPinpoint")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    response = requests.post(API_ENDPOINT, json=account_data, headers=headers)

    if response.status_code == 200:
        print("Successfully registered iCloud account with AirPinpoint")
    else:
        print(f"Error registering iCloud account: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Register iCloud account with AirPinpoint")
    parser.add_argument("api_key", help="Your AirPinpoint API key")
    args = parser.parse_args()

    register_icloud(args.api_key)