var app = angular.module('myApp', []);

app.controller('MainController', function($scope, $http) {
    $scope.isAuthenticated = false;
    $scope.credentials = {};
    $scope.newMonster = {};
    $scope.monsters = [];
    $scope.foundMonster = null; // To store the found monster

    // Mock authentication
    $scope.login = function() {
        if ($scope.credentials.username === 'user' && $scope.credentials.password === 'password') {
            $scope.isAuthenticated = true;
            $scope.fetchMonsters();
        } else {
            alert('Invalid credentials');
        }
    };

    $scope.logout = function() {
        $scope.isAuthenticated = false;
        $scope.monsters = [];
        $scope.foundMonster = null; // Reset found monster on logout
    };

    $scope.fetchMonsters = function() {
        $http.get('http://localhost:5000/monsters')  // Update to your Flask API endpoint
            .then(function(response) {
                $scope.monsters = response.data; // Store the fetched monsters
                console.log("Fetched monsters:", $scope.monsters); // Debug log
            })
            .catch(function(error) {
                console.error("Error fetching monsters:", error); // Log any errors
            });
    };

    $scope.addMonster = function() {
        $http.post('http://localhost:5000/monsters', $scope.newMonster)  // Update to your Flask API endpoint
            .then(function(response) {
                $scope.monsters.push(response.data);
                $scope.newMonster = {};
            });
    };

    $scope.deleteMonster = function(id) {
        $http.delete('http://localhost:5000/monsters/' + id)  // Corrected URL
            .then(function() {
                $scope.monsters = $scope.monsters.filter(monster => monster.id !== id);
                if ($scope.foundMonster && $scope.foundMonster.id === id) {
                    $scope.foundMonster = null; // Clear found monster if deleted
                }
            });
    };

    $scope.findMonsterById = function() {
        const monsterId = $scope.monsterIdToFind; // Get the ID from the input
        console.log("Finding monster with ID:", monsterId); // Debug log
        
        // Check if the monsterId is a valid number
        if (monsterId === undefined || monsterId === null || monsterId === '' || isNaN(monsterId)) {
            alert('Please enter a valid Monster ID.');
            return; // Exit the function if the ID is not valid
        }
    
        // Convert to integer
        const monsterIdInt = parseInt(monsterId, 10);
        console.log("Converted Monster ID:", monsterIdInt); // Debug log
    
        $http.get('http://localhost:5000/monsters/' + monsterIdInt)  // Corrected URL
            .then(function(response) {
                $scope.foundMonster = response.data; // Store the found monster
                console.log("Found Monster:", $scope.foundMonster); // Debug log
            })
            .catch(function(error) {
                alert('Monster not found!');
                $scope.foundMonster = null; // Clear found monster if not found
            });
    };
});