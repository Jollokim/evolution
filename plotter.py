import plotly.express as px
import pandas as pd
import numpy as np
import os


def plot_single_run_stats(run_file: str):

    df = pd.read_csv(run_file)

    fig = px.line(df, x="generation", y="best",
                  title='Best fitness in generation')
    fig.show()

    fig = px.line(df, x="generation", y="average",
                  title='Average fitness in generation')
    fig.show()

    fig = px.line(df, x="generation", y="standard deviation",
                  title='Standard deviation fitness in generation')
    fig.show()


def plot_all_runs_against(runs_folder: str):

    frames = get_frames(runs_folder)

    df = pd.concat(frames)

    # print(df)

    fig = px.line(df, x="generation", y="best",
                  title='Best fitness in generation', color='run')
    fig.show()

    fig = px.line(df, x="generation", y="average",
                  title='Average fitness in generation', color='run')
    fig.show()

    fig = px.line(df, x="generation", y="standard deviation",
                  title='Standard deviation fitness in generation', color='run')
    fig.show()


def plot_average_individual_runs(runs_folder: str):

    frames = get_frames(runs_folder)

    """
        Find the smallest length, don't want to start averaging on
        lower number of individual runs when some converged faster then other
    """
    smallest_len = get_fastest_generation(runs_folder)

    average_best = []
    average_avg = []
    average_std = []

    for gen in range(smallest_len):
        best_s = 0
        avg_s = 0
        std_s = 0

        for i in range(len(frames)):
            best_s += frames[i]['best'][gen]
            avg_s += frames[i]['average'][gen]
            std_s += frames[i]['standard deviation'][gen]

        best_s /= len(frames)
        avg_s /= len(frames)
        std_s /= len(frames)

        average_best.append(best_s)
        average_avg.append(avg_s)
        average_std.append(std_s)

    average_df = pd.DataFrame()

    average_df['generation'] = [i for i in range(smallest_len)]
    average_df['best'] = average_best
    average_df['average'] = average_avg
    average_df['standard deviation'] = average_std

    # print(df)

    fig = px.line(average_df, x="generation", y="best",
                  title='Best fitness in generation')
    fig.show()

    fig = px.line(average_df, x="generation", y="average",
                  title='Average fitness in generation')
    fig.show()

    fig = px.line(average_df, x="generation", y="standard deviation",
                  title='Standard deviation fitness in generation')
    fig.show()


def get_fastest_generation(runs_folder: str):
    frames = get_frames(runs_folder)

    smallest_len = len(frames[0])
    for frame in frames:
        if len(frame) < smallest_len:
            smallest_len = len(frame)

    return smallest_len


def get_average_generation(runs_folder: str):
    frames = get_frames(runs_folder)

    gens = [len(frames[i]) for i in range(len(frames))]

    return np.mean(gens)

def get_slowest_generations(runs_folder: str):
    frames = get_frames(runs_folder)

    gens = [len(frames[i]) for i in range(len(frames))]

    return np.max(gens)



def get_frames(runs_folder: str):
    frames = []

    run_c = 1

    for file in os.listdir(runs_folder):
        if file.endswith('.csv'):
            df = pd.read_csv(f'{runs_folder}/{file}')

            run = [f'run {run_c}' for i in range(len(df))]

            df['run'] = run

            frames.append(df)

            run_c += 1

    return frames
