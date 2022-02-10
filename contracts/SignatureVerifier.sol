// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin-contracts/contracts/access/Ownable.sol";
import "@openzeppelin-contracts/contracts/utils/cryptography/draft-EIP712.sol";
import "@openzeppelin-contracts/contracts/utils/cryptography/SignatureChecker.sol";

contract SignatureVerifier is EIP712, Ownable {
    uint256 value;
    uint256 publicValue;

    event PublicValueSet(address indexed setter, uint256 value);
    event ValueSet(address indexed setter, uint256 value);

    constructor(string memory name) EIP712(name, "0.0.1") {}

    function setValue(uint256 newValue) external onlyOwner {
        value = newValue;
        emit ValueSet(msg.sender, newValue);
    }

    function getValue() external view returns (uint256) {
        return value;
    }

    function setPublicValue(uint256 newValue) external {
        publicValue = newValue;
        emit PublicValueSet(msg.sender, newValue);
    }

    function getPublicValue() external view returns (uint256) {
        return publicValue;
    }

    function setValueWithSignature(
        uint256 newValue,
        uint256 blockDeadline,
        bytes memory signature
    ) external {
        bytes32 hash = getEIP712Hash(newValue, blockDeadline);
        require(
            SignatureChecker.isValidSignatureNow(owner(), hash, signature),
            "SignatureVerifier: setValueWithSignature -- Invalid signature on payload"
        );
        require(
            block.number <= blockDeadline,
            "SignatureVerifier: setValueWithSignature -- Block deadline has expired"
        );
        value = newValue;
        emit ValueSet(msg.sender, newValue);
    }

    function getEIP712Hash(uint256 newValue, uint256 blockDeadline)
        public
        view
        returns (bytes32)
    {
        bytes32 structHash = keccak256(
            abi.encode(
                keccak256("Payload(uint256 newValue,uint256 blockDeadline)"),
                newValue,
                blockDeadline
            )
        );
        bytes32 digest = _hashTypedDataV4(structHash);
        return digest;
    }
}
