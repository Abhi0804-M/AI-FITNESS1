function startSelectedExercise(selectedValue) {
    const exercisesDict = {
        "1": "Push-up",
        "2": "Pull-up",
        "3": "Squat",
        "4": "Walk",
        "5": "Sit-up",
        "6": "Jumping Jacks",
        "7": "Lunges",
        "8": "Leg Raises",
        "9": "Burpees"
        // Add more exercises as needed
    };

    const selectedExerciseId = selectedValue;
    const selectedExerciseName = exercisesDict[selectedExerciseId];

    // Send the selected exercise name to the server
    fetch(`/start-exercise/${selectedExerciseName}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if ('success' in data && data.success) {
                console.log(`Exercise "${selectedExerciseName}" started successfully.`);
            } else {
                console.error('Error:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function passSelectedExercise() {
    const selectedExerciseValue = document.getElementById('exerciseSelect').value;
    startSelectedExercise(selectedExerciseValue);
}
