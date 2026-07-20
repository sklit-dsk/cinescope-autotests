from utils.data_generator import DataGenerator

def get_movies_params():
    return {
        "minPrice": DataGenerator.generate_min_price(), 
        "locations": DataGenerator.generate_location(), 
        "published": DataGenerator.generate_published(), 
        "genreId": DataGenerator.generate_genre_id(), 
        "createdAt": DataGenerator.generate_created_at()
    }