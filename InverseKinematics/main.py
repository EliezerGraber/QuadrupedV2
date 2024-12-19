import numpy as np
import asyncio
from IK import IK

FR = [1, 60, 54, 54]
FL = [-1, 240, -54, 54]
BR = [1, -120, 54, -54]
BL = [-1, 420, -54, -54]

async def main():
	ik = IK()
	print(ik.calc(FR, 0, 150, -50))

if __name__ == "__main__":
	asyncio.run(main())