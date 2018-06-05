/*
Helper file that contains some utility methods that are commonly used.
*/
module.exports = {
    handleErrors: function(response) {
        if (!response.ok) {
            throw Error(response.statusText);
        }
        return response;
    },
    defaultBoardState: [[-4, -2, -3, -5, -6, -3, -2, -4],
                        [-1, -1, -1, -1, -1, -1, -1, -1],
                        [ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0], 
                        [ 0, 0, 0, 0, 0, 0, 0, 0], 
                        [ 1, 1, 1, 1, 1, 1, 1, 1], 
                        [ 4, 2, 3, 5, 6, 3, 2, 4]]
}

