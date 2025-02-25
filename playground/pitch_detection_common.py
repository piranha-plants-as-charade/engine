import numpy as np
import matplotlib.pyplot as plt

def generate_signal(f0, shape="exponential", noise_level=0, duration=0.5, fs=44100, n=7, sigma=1, bump_max=1, verbose=False):
    """
    Generate a signal with multiple harmonics.
    
    :param f0: fundamental frequency
    :param shape: shape of the magnitudes of the harmonics (spectral envelope)
    :param noise_level: standard deviation of the noise
    :param duration: duration of the signal in seconds
    :param fs: sampling frequency
    :param n: number of harmonics
    :param sigma: standard deviation of the Gaussian bump (only used if shape is "bump")
    :param bump_max: maximum value of the Gaussian bump (only used if shape is "bump" or "uniform")
    :return: the generated signal
    """
    magnitudes = None
    if shape == "exponential":
        magnitudes = np.exp(-np.linspace(0, 1, n))
    elif shape == "linear":
        magnitudes = np.linspace(1, 0, n)
    elif shape == "bump":
        x = np.linspace(-1, 1, n)
        bump = np.exp(- (x / sigma) ** 2)
        bump = bump / np.max(bump)
        magnitudes = bump_max * bump
    elif shape == "random":
        magnitudes = np.random.rand(n)
    elif shape == "uniform":
        magnitudes = np.ones(n) * bump_max
    else:
        raise ValueError(f"Invalid shape: {shape}")

    if verbose:
        print("Magnitudes:", magnitudes)

    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = sum([m * np.sin(2 * np.pi * f0 * t * (i+1)) for i, m in enumerate(magnitudes)])

    if noise_level > 0:
        noise = np.random.normal(0, noise_level, len(signal))
        signal += noise

    return signal

def plot_signal(signal, start=0, duration=None, fs=44100):
    """
    Plot the signal in the time domain.
    
    :param signal: the signal to plot
    :param start: start time of the window to plot in seconds
    :param duration: duration of the window to plot
    :param fs: sampling frequency
    """
    start = int(start * fs)
    if duration is not None:
        stop = start + int(duration * fs)
    else:
        stop = len(signal)
    print(start, stop)
    t = np.linspace(start, stop, stop - start, endpoint=False)
    plt.plot(t / fs, signal[start:stop])
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()
