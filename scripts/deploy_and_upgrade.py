from scripts.helpful_scripts import (
    get_account,
    encode_function_data, upgrade)
from brownie import (
    network, Box, ProxyAdmin, Contract, BoxV2, config,
    TransparentUpgradeableProxy)


def main():
    account = get_account()
    print(f"Deploying to {network.show_active}")
    box = Box.deploy({'from': account}, publish_source=True)
    print(box.retrieve())
    proxy_admin = ProxyAdmin.deploy({'from': account}, publish_source=True)

    initializer = box.store, 1
    box_encoded_initializer_functions = encode_function_data(initializer)

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_functions,
        {'from': account, 'gas_limit': 10000000}, publish_source=True)

    print(f"Proxy deployed to {proxy}, You can now upgrade to v2!")

    proxy_box = Contract.from_abi("Box", proxy.address, box.abi)
    proxy_box.store(1, {'from': account})
    box_v2 = BoxV2.deploy({'from': account}, publish_source=True)
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address,
        proxy_admin_contract=proxy_admin)
    upgrade_transaction.wait(1)
    print("Proxy has been upgraded")

    proxy_box = Contract.from_abi('BoxV2', proxy.address, BoxV2.abi)
    proxy_box.increment({'from': account})
    print(proxy_box.retrieve())
