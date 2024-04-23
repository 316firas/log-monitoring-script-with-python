#!/usr/bin/env python3
import sys
import os
import signal
import time
import matplotlib.pyplot as plt
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to monitor log file
def monitor_log(logfile):
    logger.info(f"Monitoring log file: {logfile}")
    timestamps = []
    error_counts = []
    with open(logfile, 'r') as file:
        while True:
            line = file.readline()
            if line:
                logger.info(line.strip())  # Log each line as INFO
                timestamp = time.time()
                timestamps.append(timestamp)
                error_counts.append(line.lower().count("error"))
                # Update plot
                plt.plot(timestamps, error_counts, color='b')
                plt.xlabel('Time')
                plt.ylabel('Error Count')
                plt.title('Real-time Error Count')
                plt.pause(0.05)  # Update plot every 0.05 seconds
            else:
                time.sleep(0.1)

# Function to analyze log file
def analyze_log(logfile):
    logger.info(f"Analyzing log file: {logfile}")
    error_count = 0
    with open(logfile, 'r') as file:
        for line in file:
            if "error" in line.lower():
                error_count += 1
    logger.info(f"Number of errors: {error_count}")

# Signal handler to stop monitoring
def signal_handler(sig, frame):
    logger.info("Exiting...")
    sys.exit(0)

# Main function
def main():
    if len(sys.argv) != 2:
        logger.error(f"Usage: {sys.argv[0]} <logfile>")
        sys.exit(1)

    logfile = sys.argv[1]
    if not os.path.isfile(logfile):
        logger.error(f"Error: Log file not found: {logfile}")
        sys.exit(1)

    # Trap Ctrl+C to stop monitoring
    signal.signal(signal.SIGINT, signal_handler)

    # Create a real-time error count plot
    plt.ion()
    plt.figure()
    plt.show()

    # Monitor log file continuously
    monitor_log(logfile)

    # Analyze log file
    analyze_log(logfile)

if __name__ == "__main__":
    main()
