import numpy as np
import asyncio
from IK import IK

FR = [1, 60, 54, 54]
FL = [1, -60, -54, 54]
BL = [1, -120, -54, -54]
BR = [1, -210, 54, -54]

async def main():
	ik = IK()
	print(ik.calc(BL, -54, -150, -50))

if __name__ == "__main__":
	asyncio.run(main())