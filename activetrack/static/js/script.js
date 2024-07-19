/*jshint esversion: 6 */

document.addEventListener("DOMContentLoaded", function() {
    // depending on whether 'strength' or 'endurance' is chosen as a workout type when adding an activity
    // the related exercises will populate the exercise drop down box

    // Grab the elements of the workout type and exercise drop downs
    const workoutType = document.getElementById("workout_type");
    const exerciseName = document.getElementById("exercise_name");

    if (workoutType && exerciseName) {
        const updateExercises = function(exercises) {
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
        };

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
        
        // Function that changes the add activity form fields depending on what workout type is selected
        // Adds or removes the required attribute depending on if the field is shown
        const formFieldToggler = function() {
            const chosenWorkoutType = workoutType.value;
            const strengthFields = document.getElementsByClassName('strength_field');
            const enduranceFields = document.getElementsByClassName('endurance_field');

            if (chosenWorkoutType === 'endurance') {
                for (let i = 0; i < strengthFields.length; i++) {
                    strengthFields[i].style.display = 'none';
                    strengthFields[i].removeAttribute('required');
                }
                for (let i = 0; i < enduranceFields.length; i++) {
                    enduranceFields[i].style.display = 'block';
                    enduranceFields[i].setAttribute('required', "");
                }
            } else {
                for (let i = 0; i < strengthFields.length; i++) {
                    strengthFields[i].style.display = 'block';
                    strengthFields[i].setAttribute('required', "");
                }
                for (let i = 0; i < enduranceFields.length; i++) {
                    enduranceFields[i].style.display = 'none';
                    enduranceFields[i].removeAttribute('required');
                }
            }
        };

        // Call the function to change the form fields on page load
        formFieldToggler();
        // When the workout type is changed, the function is called to change the form fields
        workoutType.addEventListener('change', formFieldToggler);
    }
});