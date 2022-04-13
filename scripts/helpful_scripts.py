from brownie import accounts, network, config
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local', 'mainnet-fork']
FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork-dev',
                             'development', 'mainnet-fork']


def upgrade(account, proxy,
            new_implementation_address,
            proxy_admin_contract=None,
            initializer=None, *args
            ):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address, new_implementation_address,
                encode_function_call, {'from': account}
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address,
                {'from': account}
            )
    else:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implementation_address,
                encode_function_call,
                {'from': account})
        else:
            transaction = proxy.upgradeTo(
                new_implementation_address, {'from': account})
    return transaction


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr='0x')
    return initializer.encode_input(*args)


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active(
    ) in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config['wallets']['from_key'])
