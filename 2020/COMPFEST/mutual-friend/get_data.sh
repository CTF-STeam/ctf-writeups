#!/bin/bash
python -c "for i in range(2000): print(i)" | nc 128.199.157.172 27268 >> data.txt

