import numpy as np


def calibrate_single_phase(phases):
    """
    Calibrate phase data from the single time moment
    Based on:
        https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/sys031fp.pdf
        https://github.com/ermongroup/Wifi_Activity_Recognition/.../phase_calibration.m

    :param phases: phase in the single time moment, np.array of shape(1, num of subcarriers)
    :return: calibrate phase, np.array of shape(1, num of subcarriers)
    """

    phases = np.array(phases)
    difference = 0

    calibrated_phase, calibrated_phase_final = np.zeros_like(phases), np.zeros_like(phases)
    calibrated_phase[0] = phases[0]

    phases_len = phases.shape[0]

    for i in range(1, phases_len):
        temp = phases[i] - phases[i - 1]

        if abs(temp) > np.pi:
            difference = difference + 1 * np.sign(temp)

        calibrated_phase[i] = phases[i] - difference * 2 * np.pi

    k = (calibrated_phase[-1] - calibrated_phase[0]) / (phases_len - 1)
    b = np.mean(calibrated_phase)

    for i in range(phases_len):
        calibrated_phase_final[i] = calibrated_phase[i] - k * i - b

    return calibrated_phase_final


def calibrate_phase(phases):
    """
    Calibrate phase data based on the following method:
        https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/sys031fp.pdf
        https://github.com/ermongroup/Wifi_Activity_Recognition/.../phase_calibration.m

    :param phases: np.array of shape(data len, num of subcarries)
    :return: calibrated phases: np.array of shape(data len, num of subcarriers)
    """

    calibrated_phases = np.zeros_like(phases)

    for i in range(phases.shape[0]):
        calibrated_phases[i] = calibrate_single_phase(np.unwrap(phases[i]))

    return calibrated_phases


def calibrate_amplitude(amplitudes, rssi=1):
    """
    Simple amplitude normalization, that could be multiplied by rsii
    ((data - min(data)) / (max(data) - min(data))) * rssi

    :param amplitudes: np.array of shape(data len, num of subcarriers)
    :param rssi: number
    :return: normalized_amplitude: np.array of shape(data len, num of subcarriers)
    """

    amplitudes = np.array(amplitudes)
    return ((amplitudes - np.min(amplitudes)) / (np.max(amplitudes) - np.min(amplitudes))) * rssi