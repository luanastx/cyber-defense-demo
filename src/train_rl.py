#!/usr/bin/env python3
import argparse
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from src.rl_env import FlowBlockEnv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help=".npz com X e y")
    parser.add_argument("--output", default="output/rl.zip")
    args = parser.parse_args()
    data = np.load(args.input)
    X = data["X"]
    y = data["y"]
    env = DummyVecEnv([lambda: FlowBlockEnv(X, y)])
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=20000)
    model.save(args.output)
    print(f"Saved RL agent to {args.output}")

if __name__ == "__main__":
    main()