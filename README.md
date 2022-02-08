# bureaucrat

This repository demonstrates how to implement and use [EIP712](https://eips.ethereum.org/EIPS/eip-712) for
message signing.

It implements a simple contract called [`SignatureVerifier`](./contracts/SignatureVerifier.sol) which
contains a `value` state variable (which is a `uint256`).

`SignatureVerifier` is ownable, and the owner of the contract may call the `setValue` method to set this
value to whatever they like.

`SignatureVerifier` also includes a `setValueWithSignature` method that allows any client to set the
value *provided* they have a signed message from the contract owner certifying that the value they would
like to set is approved and that they are setting the value before a given block deadline.

`SignatureVerifier` also includes a public view function called `getEIP712Hash` which calculates the message hash
for a given payload to `setValueWithSignature`. This is a convenience which allows server implementations to
forego implementing the serialization logic for messages (which depends on the contracts EIP712 domain separator).

## Setting up your environment

First set up a Python 3 virtual environment. Please use Python > 3.6.

```
python3 -m venv .bureaucrat
```

Activate your virtual environment

```
source .bureaucrat/bin/activate
```

Install dependencies:

```
pip install -e ".[dev]"
```

Compile smart contract:

```
brownie compile
```

## Workflow

Deploy the contract:

```
bureaucrat contract deploy --network mumbai --sender .secrets/dao-dev.json --password peppercat --name PaperPusher
```

Store the address of the deployed contract in the `CONTRACT_ADDRESS` variable.

Sign a message as owner specifying a new value and block deadline (`$FUTURE_BLOCK`):

```
SIGNED_MESSAGE=$(bureaucrat sign --network mumbai --address $CONTRACT_ADDRESS --signer .secrets/dao-dev.json --new-value 42 --block-deadline $FUTURE_BLOCK  --password peppercat)
```

Submit signed message as client to change the value:

```
bureaucrat contract set-value-with-signature \
    --network mumbai \
    --address $CONTRACT_ADDRESS \
    --sender .secrets/test-account.json \
    --password peppercat \
    --new-value 42 \
    --block-deadline $FUTURE_BLOCK \
    --signature "$SIGNED_MESSAGE"
```

This transaction will fail if `--new-value` is set to anything other than the one in the signed payload,
if `--block-deadline` is set to anything other than the one in the signed payload, or if the block deadline
has already expired.
