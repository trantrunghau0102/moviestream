// Chuyển sang database movie-streaming
db = db.getSiblingDB('movie-streaming');

// Xóa dữ liệu cũ nếu có
db.movies.drop();

// Tạo indexes cho hiệu năng tốt hơn
db.movies.createIndex({ "title": "text" });
db.movies.createIndex({ "createdAt": -1 });
db.movies.createIndex({ "views": -1 });
db.movies.createIndex({ "rating": -1 });

// Mảng chứa dữ liệu mẫu
const sampleMovies = [
    {
        title: "Ocean View",
        originalTitle: "Ocean View (2024)",
        description: "Khám phá vẻ đẹp kỳ diệu của đại dương với những cảnh quay tuyệt đẹp về san hô và sinh vật biển.",
        videoUrl: "videos/ocean-view.mp4",
        duration: 45,
        thumbnail: "https://via.placeholder.com/300x450?text=Ocean+View",
        genre: ["Nature", "Documentary"],
        rating: 4.5,
        year: 2024,
        country: "Vietnam",
        director: "Nguyen Van A",
        cast: [
            {
                name: "Nature",
                character: "Herself",
                image: "https://via.placeholder.com/150?text=Nature"
            }
        ],
        status: "Released",
        views: 1200,
        releaseDate: "2024-01-15",
        createdAt: new Date(),
        updatedAt: new Date()
    },
    {
        title: "Mountain Adventure",
        originalTitle: "Mountain Adventure (2024)",
        description: "Hành trình chinh phục đỉnh núi cao với những thử thách và khung cảnh ngoạn mục.",
        videoUrl: "videos/mountain-scene.mp4",
        duration: 55,
        thumbnail: "https://via.placeholder.com/300x450?text=Mountain+Adventure",
        genre: ["Adventure", "Documentary"],
        rating: 4.8,
        year: 2024,
        country: "Vietnam",
        director: "Nguyen Van B",
        cast: [
            {
                name: "Mountain Explorer",
                character: "Guide",
                image: "https://via.placeholder.com/150?text=Explorer"
            }
        ],
        status: "Released",
        views: 800,
        releaseDate: "2024-02-01",
        createdAt: new Date(),
        updatedAt: new Date()
    }
];

// Insert dữ liệu mẫu
try {
    const result = db.movies.insertMany(sampleMovies);
    print('Inserted sample movies successfully:', result);
} catch (error) {
    print('Error inserting sample movies:', error);
}