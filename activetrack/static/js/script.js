document.addEventListener("DOMContentLoaded", function() {
    // depending on whether 'strength' or 'endurance' is chosen as a workout type when adding an activity
    // the related exercises will populate the exercise drop down box

    // Grab the elements of the workout type and exercise drop downs
    const workoutType = document.getElementById("workout_type");
    const exerciseName = document.getElementById("exercise_name");

    function updateExercises(exercises) {
        const selectedType = workoutType.value;
        exerciseName.innerHTML = "";

        // Filters the exercises in the json file depending on what workout type is selected
        const filteredExercises = exercises.filter(exercise => exercise.exercise_type === selectedType);

        // Populates the exercises dropdown with the filtered exercises
        filteredExercises.forEach(exercise => {
            const option = document.createElement("option");
            option.value = exercise.exercise_name;
            option.textContent = exercise.exercise_name;
            exerciseName.appendChild(option);
        });
    }

    // Fetches the exercises from the get_exercises route when the workout type is changed
    workoutType.addEventListener("change", function() {
        fetch('/get_exercises')
            .then(response => response.json())
            .then(data => updateExercises(data))
            .catch(error => console.error('Error fetching exercises:', error));
    });

    // Fetches the exercises from the get_exercises route on load
    fetch('/get_exercises')
        .then(response => response.json())
        .then(data => updateExercises(data))
        .catch(error => console.error('Error fetching exercises:', error));
});