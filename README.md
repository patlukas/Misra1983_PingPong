# Misra Algorithm Implementation

## Overview

This project implements Mutual Exclusion within a Ring Topology using the Misra algorithm. It is method for ensuring that only one node at a time enters the critical section in a distributed system.

## Features

- **UDP and TCP Communication:** Implements both UDP and TCP socket connections.
- **Token-Passing Mechanism:** Uses ping-pong messages to coordinate access to the critical section.
- **Node Recovery:** Handles message loss and reconstructs missing tokens.
- **Critical Section Execution:** Simulates access to a critical section.
- **Keyboard Interaction:** Allows intentional message loss simulation using keyboard inputs (`i` for PING, `o` for PONG).

## Prerequisites

- Python 3.x
- Required libraries: `socket`, `threading`, `time`, `sys`, `keyboard`
- Install missing dependencies using:
  ```bash
  pip install keyboard
  ```

## How to Run

To start a node in the network, use the following command:

```bash
python misra_algorithm.py <my_ip> <my_port> <next_ip> <next_port> <special_mode>
```

### Arguments:

- `<my_ip>`: IP address of the current node.
- `<my_port>`: Port number of the current node.
- `<next_ip>`: IP address of the next node in the ring.
- `<next_port>`: Port number of the next node in the ring.
- `<special_mode>`: Set to `1` for the first node in the network to initiate the process; otherwise, set to `0`.

### Example Execution:

```bash
python misra_algorithm.py 127.0.0.1 5000 127.0.0.1 5001 1
python misra_algorithm.py 127.0.0.1 5001 127.0.0.1 5002 0
python misra_algorithm.py 127.0.0.1 5002 127.0.0.1 5000 0
```

## How It Works

1. Nodes communicate via UDP or TCP sockets.
2. A **ping-pong** token system is used to maintain control over the critical section.
3. The first node in the ring starts with the `special_mode` flag set to `1`.
4. Tokens (`PING` and `PONG`) are passed around in a cyclic order.
5. When a node receives a `PING`, it enters the **critical section**, executes it, and then forwards the token.
6. The algorithm supports failure handling and token regeneration.

## Selecting TCP or UDP Connection

To choose whether the algorithm should use **TCP** or **UDP** for communication, change the parent class of the `PingPong` class.

- For UDP: `class PingPong(PingPongConnectionUDP)`
- For TCP: `class PingPong(PingPongConnectionTCP)`

## Simulating Token Loss

- Press `i` to simulate **PING loss**.
- Press `o` to simulate **PONG loss**.

## Notes

- Ensure that all nodes are properly connected in a ring topology.
- The program runs in an infinite loop until manually terminated.
$(basename git rev-parse --show-toplevel)
![](github.ct8.pl/readme/patlukas/Misra1983_PingPong)
