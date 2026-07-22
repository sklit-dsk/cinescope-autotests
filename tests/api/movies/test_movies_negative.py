class TestMoviesNegative:
    def test_get_movies_with_bad_params(self, api_manager, bad_movie_params):
        response = api_manager.movies_api.get_movies(expected_status = 400, params=bad_movie_params)
        response_data = response.json()

        assert response_data["statusCode"] == 400
        assert response_data["error"]

    def test_create_movie_with_bad_params(self, movie_data, super_admin):
        movie_data["name"] = 432423
        movie_data["price"] = "dddq"
        movie_data["description"] = 133

        response = super_admin.api.movies_api.create_movie(
            movie_data, expected_status=400
        )

        assert response.status_code == 400

    def test_create_existing_movie(self, created_movie, super_admin, movie_data):

        response = created_movie.json()
        super_admin.api.movies_api.create_movie(movie_data, expected_status=409)

        assert response["name"] == movie_data["name"]

    def test_get_non_existent_movie(self, super_admin, created_movie):
        response = created_movie.json()
        response_delete_movie = super_admin.api.movies_api.delete_movie_by_id(
            movie_id=response["id"]
        )
        response_get_deleted_movie = super_admin.api.movies_api.get_movie_by_id(
            movie_id=response_delete_movie.json()["id"], expected_status=404
        )

        assert response_get_deleted_movie.json()["statusCode"] == 404

    def test_delete_non_existent_movie(self, super_admin, created_movie):
        response = created_movie.json()
        super_admin.api.movies_api.delete_movie_by_id(movie_id=response["id"])
        response_delete_non_existent_movie = (
            super_admin.api.movies_api.delete_movie_by_id(
                movie_id=response["id"], expected_status=404
            )
        )

        assert response_delete_non_existent_movie.status_code == 404
