# Vercel Deployment Guide

## Fixed Configuration Files

### 1. `api/index.py`
This file serves as the serverless function entry point for Vercel. It:
- Sets up the Django application
- Exports the WSGI application as `app` (required by Vercel Python runtime)

### 2. `vercel.json`
Configuration for Vercel deployment:
- Uses `functions` to define the serverless function
- Routes all requests to `/api/index.py`
- Handles static and media files
- Sets environment variables

### 3. `hospital/settings.py`
Updated to:
- Use environment variables for `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`
- Allow all hosts by default (can be restricted via environment variables)

## Deployment Steps

1. **Commit and push all changes to GitHub**
   ```bash
   git add .
   git commit -m "Fix Vercel deployment configuration"
   git push origin main
   ```

2. **Set Environment Variables in Vercel Dashboard**
   - Go to your project settings in Vercel
   - Navigate to "Environment Variables"
   - Add the following:
     - `SECRET_KEY`: A secure random string (generate one)
     - `DEBUG`: Set to `False` for production
     - `ALLOWED_HOSTS`: Your Vercel domain (e.g., `your-app.vercel.app`)
     - `DJANGO_SETTINGS_MODULE`: `hospital.settings` (already in vercel.json)

3. **Redeploy on Vercel**
   - The deployment should automatically trigger after pushing to GitHub
   - Or manually trigger a new deployment from Vercel dashboard

## Important Notes

- **Database**: SQLite is used, which has limitations on serverless platforms. Consider using PostgreSQL (via Vercel Postgres or external service) for production.
- **Static Files**: Collected to `staticfiles` directory during build
- **Media Files**: Consider using cloud storage (AWS S3, Cloudinary) for production

## Troubleshooting

If you still get errors:
1. Check that `api/index.py` exists and exports `app`
2. Verify `vercel.json` syntax is correct (no trailing commas)
3. Ensure all dependencies are in `requirements.txt`
4. Check Vercel build logs for specific errors
