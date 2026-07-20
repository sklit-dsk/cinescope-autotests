from utils.data_generator import DataGenerator

class TestMovies:
    def test_get_movies_without_params(self, api_manager):
        response = api_manager.movies_api.get_movies()
        response_data = response.json()
        
        assert "count" in response_data
        assert response_data["movies"]
        
    def test_get_movies_with_params(self, api_manager, movie_params):
        response = api_manager.movies_api.get_movies(params=movie_params)
        response_data = response.json()
        
        assert "movies" in response_data
        assert "count" in response_data
        
    def test_create_movie(self, created_movie):
        response = created_movie.json()
        assert response["createdAt"]
        
        
    def test_get_movie_by_id(self, api_manager, created_movie):
        response = created_movie
        response_movie = api_manager.movies_api.get_movie_by_id(movie_id = response.json()["id"], expected_status = 200)
        
        assert response.json()["id"] == response_movie.json()["id"]
        
    def test_delete_movie(self, api_manager, created_movie):
        response = created_movie.json()
        response_delete_movie = api_manager.movies_api.delete_movie_by_id(movie_id = response["id"])
        response_get_deleted_movie = api_manager.movies_api.get_movie_by_id(movie_id = response_delete_movie.json()["id"], expected_status = 404)
        
        assert response_get_deleted_movie.json()["statusCode"] == 404
        
    def test_patch_movie(self, api_manager, created_movie, movie_data):
        response = created_movie.json()
        new_movie_data = movie_data.copy()
        new_movie_data["name"] = DataGenerator.generate_movie_name()
        new_movie_data["price"] = DataGenerator.generate_min_price()
        response_patch_movie = api_manager.movies_api.patch_movie_by_id(movie_id = response["id"], data = new_movie_data)
        response_get_patched_movie = api_manager.movies_api.get_movie_by_id(movie_id = response_patch_movie.json()["id"], expected_status = 200)
        
        assert response_get_patched_movie.json()["name"] == response_patch_movie.json()["name"]
        assert response_get_patched_movie.json()["price"] == response_patch_movie.json()["price"]
        assert response_patch_movie.status_code == 200