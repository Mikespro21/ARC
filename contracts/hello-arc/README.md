# hello-arc (Foundry)

This is a minimal Foundry project configured for **Arc Testnet**.

## 1) Configure environment

Create a `.env` in this directory:

```bash
cp .env.example .env
```

Then **edit** `PRIVATE_KEY` and (later) `HELLOARCHITECT_ADDRESS`.

Load env vars:

```bash
source .env
```

## 2) Install Foundry dependencies

From this directory:

```bash
forge install foundry-rs/forge-std --no-commit
```

## 3) Test and build

```bash
forge test
forge build
```

## 4) Deploy to Arc Testnet

Fund the deployer with testnet USDC (Arc gas token) via Circle faucet, then:

```bash
forge create src/HelloArchitect.sol:HelloArchitect \
  --rpc-url $ARC_TESTNET_RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast
```

## 5) Interact

```bash
cast call $HELLOARCHITECT_ADDRESS "getGreeting()(string)" --rpc-url $ARC_TESTNET_RPC_URL
```
