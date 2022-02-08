import argparse

from brownie import network
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
    message_from_contract = contract.get_eip712_hash(
        args.new_value, args.block_deadline
    )
    print("From contract:", message_from_contract)
    message = Payload(
        _name_="PaperPusher",
        _version_="0.0.1",
        _chainId_=80001,
        _verifyingContract_=args.address,
        newValue=args.new_value,
        blockDeadline=args.block_deadline,
    )
    signed_message = signer.sign_message(message)
    print("Message hash:", signed_message.messageHash.hex())
    print("Signature:", signed_message.signature.hex())


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
