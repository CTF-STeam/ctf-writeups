@echo off

for /l %%x in (1, 1, 500) do (
   echo %%%x
   nc mtp.chujowyc.tf 4003 >> mtp_in.txt
)
