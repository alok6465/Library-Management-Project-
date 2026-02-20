# 🎉 Festival Feature Guide

## Overview
The Festival feature allows the library to showcase celebrations, events, and special occasions with beautiful animations and media support.

## Features

### For Students:
- ✅ View all active festivals with animated cards
- ✅ See festival images and descriptions
- ✅ Watch festival videos (YouTube support)
- ✅ Cool floating festival button with bounce animation
- ✅ Responsive design for all devices
- ✅ Smooth hover effects and transitions

### For Admins:
- ✅ Add new festivals with images and videos
- ✅ Manage all festivals (activate/deactivate)
- ✅ Delete festivals
- ✅ Upload festival images
- ✅ Add YouTube video links
- ✅ Set festival dates

## How to Use

### Admin - Adding a Festival:

1. **Login as Admin**
2. **Go to Admin Dashboard**
3. **Click "Festivals" button**
4. **Click "Add New Festival"**
5. **Fill in details:**
   - Festival Title (e.g., "World Book Day 2024")
   - Festival Date
   - Description
   - Upload Image (optional)
   - Add Video URL (YouTube link, optional)
6. **Click "Add Festival"**

### Admin - Managing Festivals:

**Activate/Deactivate:**
- Click the "Activate" or "Deactivate" button
- Only active festivals are visible to students

**Delete:**
- Click the "Delete" button
- Confirm deletion

### Students - Viewing Festivals:

1. **Click "Festivals" in navigation menu**
2. **Browse all active festivals**
3. **Click "Watch Video" to see festival videos**
4. **Use floating festival button (🎉) for quick access**

## Animations

### Card Animations:
- Slide-in animation on page load
- Hover lift effect
- Image zoom on hover
- Pulse animation on badges

### Floating Button:
- Bounce animation
- Hover scale effect
- Fixed position for easy access

### Hero Section:
- Gradient background
- Floating emoji animation
- Responsive design

## File Structure

```
app/
├── static/
│   ├── css/
│   │   └── festival.css (festival animations)
│   └── festivals/ (festival images)
├── templates/
│   └── main/
│       ├── festivals.html (student view)
│       ├── manage_festivals.html (admin management)
│       └── add_festival.html (add festival form)
└── models.py (Festival model)
```

## Database Schema

### Festival Model:
- `id` - Primary key
- `title` - Festival name
- `description` - Festival details
- `date` - Festival date
- `image_path` - Path to festival image
- `video_url` - YouTube or video URL
- `created_by` - Admin who created it
- `created_at` - Creation timestamp
- `is_active` - Active/Inactive status

## CSS Animations

### Available Animations:
- `float` - Floating effect
- `pulse` - Pulsing effect
- `bounce` - Bouncing effect
- `slideInUp` - Slide in from bottom
- `confetti-fall` - Confetti falling effect

## Video Support

### Supported Platforms:
- YouTube (auto-converts to embed)
- Direct video URLs
- Embedded iframe support

### Video Modal:
- Full-screen video player
- Responsive design
- Auto-pause on close

## Tips

### For Best Results:
1. **Image Size:** 1200x800px recommended
2. **Image Format:** JPG, PNG, GIF
3. **Video:** Use YouTube links for best compatibility
4. **Description:** Keep under 200 characters for card view
5. **Date:** Set accurate dates for proper sorting

### Example Festivals:
- World Book Day
- Library Week
- Reading Marathon
- Author Meet & Greet
- Book Fair
- Literary Festival
- Knowledge Day
- Independence Day Celebration

## Troubleshooting

### Images not showing?
- Check if `/static/festivals/` directory exists
- Verify image file permissions
- Ensure images are in supported formats

### Videos not playing?
- Use YouTube links (https://youtube.com/watch?v=...)
- Check video privacy settings
- Ensure video URL is correct

### Animations not working?
- Clear browser cache
- Check if `festival.css` is loaded
- Verify Bootstrap 5 is included

## Future Enhancements

Possible additions:
- Gallery view with multiple images
- Event registration
- Calendar integration
- Social media sharing
- Comments section
- Photo upload by students

---

**Enjoy celebrating with your library community! 🎊📚**
