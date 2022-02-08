import argparse

from brownie import network
from eth_account._utils.signing import sign_message_hash
import eth_keys
from hexbytes import HexBytes
from eip712.messages import EIP712Message

from . import SignatureVerifier


class Payload(EIP712Message):
    _name_: "string"
    _version_: "string"
    _chainId_: "uint256"
    _verifyingContract_: "address"

    newValue: "uint256"
    blockDeadline: "uint256"


def sign_message(args: argparse.Namespace) -> None:
    network.connect(args.network)
    signer = network.accounts.load(args.signer, args.password)
    contract = SignatureVerifier.SignatureVerifier(args.address)
    message = contract.get_eip712_hash(args.new_value, args.block_deadline)
    # Brownie required us to use the EIP712Message class which doesn't make it easy to use the message
    # hash returned by the contract. I dug into the internals of the brownie "sign_message" code to come
    # up with this.
    # See: https://github.com/eth-brownie/brownie/blob/af0be999c348cbba83c9f331da6a3dde96d0e007/brownie/network/account.py#L931
    eth_private_key = eth_keys.keys.PrivateKey(HexBytes(signer.private_key))
    message_hash_bytes = HexBytes(message)
    _, _, _, signed_message_bytes = sign_message_hash(
        eth_private_key, message_hash_bytes
    )
    print(signed_message_bytes.hex())


def main():
    parser = argparse.ArgumentParser(
        description="bureaucrat: Signature verification on Solidity smart contracts"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    contract_parser = SignatureVerifier.generate_cli()
    subparsers.add_parser("contract", parents=[contract_parser], add_help=False)

    sign_parser = subparsers.add_parser("sign")
    sign_parser.add_argument(
        "--network", required=True, help="Brownie network to connect to"
    )
    sign_parser.add_argument(
        "--address",
        required=True,
        help="Address of deployed contract (to get message hash)",
    )
    sign_parser.add_argument(
        "--signer", required=True, help="Path to keystore file for signer"
    )
    sign_parser.add_argument(
        "--password", default=None, help="Optional password to signer keyfile"
    )
    sign_parser.add_argument(
        "--new-value", required=True, type=int, help="New value to sign"
    )
    sign_parser.add_argument(
        "--block-deadline",
        required=True,
        type=int,
        help="Block deadline for signed message",
    )
    sign_parser.set_defaults(func=sign_message)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
