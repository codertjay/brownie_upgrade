from scripts.helpful_scripts import get_account, encode_function_data
from brownie import (Box,
                     ProxyAdmin,
                     TransparentUpgradeableProxy,
                     Contract,
                     config,
                     network)


def test_proxy_delegate_calls():
    account = get_account()
    box = Box.deploy({'from': account})
    proxy_admin = ProxyAdmin.deploy({'from': account},
                                    publish_source=config['networks'][
                                        network.show_active()].get('verify', False))
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {'from': account},
        publish_source=config['networks'][
            network.show_active()].get('verify', False))
    proxy_box = Contract.from_abi('Box', proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {'from': account})
    assert proxy_box.retrieve() == 1
