import sys
import librosa
import pretty_midi
import numpy as np
import concurrent.futures

def convert_mp3_to_midi(mp3_path, midi_path):
    print("Loading audio file...")
    # Load audio
    y, sr = librosa.load(mp3_path)
    print(f"Audio loaded: {len(y)/sr:.2f} seconds at {sr} Hz")
    
    print("Processing onset detection and pitch extraction in parallel...")
    # Use threads for parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_onset = executor.submit(librosa.onset.onset_detect, y=y, sr=sr, units='frames')
        future_pitch = executor.submit(librosa.pyin, y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr)
        
        onset_frames = future_onset.result()
        f0, voiced_flag, voiced_probs = future_pitch.result()
    
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    print(f"Detected {len(onset_times)} onsets")
    print("Pitch extraction complete")
    
    print("Grouping into notes...")
    # Group into notes based on onsets
    notes = []
    for i in range(len(onset_times) - 1):
        start_time = onset_times[i]
        end_time = onset_times[i+1]
        start_frame = librosa.time_to_frames(start_time, sr=sr)
        end_frame = librosa.time_to_frames(end_time, sr=sr)
        pitches_in_interval = f0[start_frame:end_frame]
        voiced = voiced_flag[start_frame:end_frame]
        if np.any(voiced):
            avg_pitch = np.mean(pitches_in_interval[voiced])
            if not np.isnan(avg_pitch):
                midi_note = int(round(librosa.hz_to_midi(avg_pitch)))
                notes.append((start_time, end_time, midi_note))
    
    # Last note
    if len(onset_times) > 0:
        start_time = onset_times[-1]
        end_time = len(y) / sr
        start_frame = librosa.time_to_frames(start_time, sr=sr)
        pitches_in_interval = f0[start_frame:]
        voiced = voiced_flag[start_frame:]
        if np.any(voiced):
            avg_pitch = np.mean(pitches_in_interval[voiced])
            if not np.isnan(avg_pitch):
                midi_note = int(round(librosa.hz_to_midi(avg_pitch)))
                notes.append((start_time, end_time, midi_note))
    
    print(f"Extracted {len(notes)} notes")
    
    print("Creating MIDI file...")
    # Create MIDI
    midi = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    for start, end, note in notes:
        note_obj = pretty_midi.Note(velocity=100, pitch=note, start=start, end=end)
        piano.notes.append(note_obj)
    midi.instruments.append(piano)
    midi.write(midi_path)
    print("MIDI file created")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_mp3_to_midi.py <mp3_file> <midi_file>")
        sys.exit(1)
    mp3_file = sys.argv[1]
    midi_file = sys.argv[2]
    convert_mp3_to_midi(mp3_file, midi_file)
    print(f"Converted {mp3_file} to {midi_file}")