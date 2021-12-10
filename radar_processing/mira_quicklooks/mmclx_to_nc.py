ncfile = ncfile.sortby(
    [
        "base_time",
        "time_offset",
        "signal_to_noise_ratio",
        "reflectivity",
        "filtered_reflectivity",
        "velocity",
        "filtered_velocity",
        "linear_depolarization_ratio",
        "filtered_linear_depolarization_ratio",
        "cross_correlation_ratio",
        "differential_phase",
        "nyquist_velocity",
        "n_fft",
        "prf",
        "prt",
        "n_range_gates",
        "range_resolution",
        "n_samples",
        "pulse_width",
        "frequency",
        "latitude",
        "longitude",
        "altitude",
    ]
)

