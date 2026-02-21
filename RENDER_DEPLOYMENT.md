# Deploy Library Management System to Render

## Step-by-Step Deployment Guide

### Prerequisites
- GitHub account with your project repository
- Render account (free tier available at https://render.com)

### Your GitHub Repository
**Repository URL:** https://github.com/alok6465/Library-Management-Project-

---

## Deployment Steps

### 1. Sign Up / Login to Render
1. Go to https://render.com
2. Click "Get Started" or "Sign In"
3. Sign up with GitHub (recommended) or email

### 2. Create New Web Service
1. Click "New +" button in top right
2. Select "Web Service"
3. Connect your GitHub account if not already connected
4. Search for "Library-Management-Project-" repository
5. Click "Connect"

### 3. Configure Web Service

Fill in the following settings:

**Basic Settings:**
- **Name:** `library-management-system` (or any name you prefer)
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt, Singapore)
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `chmod +x build.sh && ./build.sh`
- **Start Command:** `gunicorn run:app`

**Instance Type:**
- Select **Free** (for testing) or **Starter** ($7/month for better performance)

### 4. Environment Variables
Click "Advanced" and add these environment variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `your-secret-key-here-change-this` |
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.11.0` |

**Important:** Change the SECRET_KEY to a random string for security!

### 5. Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Watch the logs for any errors

### 6. Access Your Application
Once deployed, you'll get a URL like:
```
https://library-management-system.onrender.com
```

---

## Post-Deployment Setup

### Create Admin Account
1. Visit: `https://your-app.onrender.com/create-demo-data`
2. This creates sample users and books
3. Login with admin credentials shown on the page

### Default Login Credentials
After running `/create-demo-data`:

**Admin:**
- PRN: `ADM2024001`
- Password: `Usha25061975`

**Student:**
- PRN: `PRN2024001`
- Password: `Sunita15081995`

---

## Troubleshooting

### Common Issues

**1. Build Failed**
- Check Python version in environment variables
- Verify all dependencies in requirements.txt
- Check build logs for specific errors

**2. Application Crashes**
- Check runtime logs in Render dashboard
- Verify database is created properly
- Check SECRET_KEY is set

**3. Database Not Found**
- Re-run build command
- Check build.sh executed successfully
- Visit `/create-demo-data` to initialize

**4. Static Files Not Loading**
- Render serves static files automatically
- Check file paths are correct
- Clear browser cache

### View Logs
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. Check for errors

---

## Important Notes

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for one service)

### Database Persistence
- SQLite database persists on Render's disk
- Data is preserved between deployments
- For production, consider PostgreSQL

### Upgrade to Paid Plan
For better performance:
1. Go to service settings
2. Change instance type to "Starter" ($7/month)
3. Service stays always active
4. Faster response times

---

## Updating Your Application

### Push Updates
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render automatically redeploys when you push to GitHub!

---

## Custom Domain (Optional)

### Add Your Domain
1. Go to service settings
2. Click "Custom Domains"
3. Add your domain
4. Update DNS records as shown
5. Wait for SSL certificate (automatic)

---

## Support

### Need Help?
- Check Render docs: https://render.com/docs
- View logs in Render dashboard
- Check GitHub repository issues
- Contact: Your email/support

---

## Security Checklist

✅ Change SECRET_KEY in environment variables
✅ Use strong admin passwords
✅ Enable HTTPS (automatic on Render)
✅ Keep dependencies updated
✅ Monitor logs regularly

---

## Success! 🎉

Your Library Management System is now live!

**Share your URL:**
`https://your-app-name.onrender.com`

**Features Available:**
- Student login and book borrowing
- Admin dashboard and management
- Festival announcements
- Virtual books
- Excel exports
- And more!

---

**Deployed from:** https://github.com/alok6465/Library-Management-Project-
