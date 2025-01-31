import click
from sqlalchemy import create_engine, text

@click.command()
@click.option('--limit', default=10, help='Number of images to show')
def show_cached_images(limit):
    """Show cached images from database"""
    engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
    
    query = text(f"""
        SELECT asin, image_url, last_updated 
        FROM product_images 
        ORDER BY last_updated DESC 
        LIMIT :limit
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})
        
        click.echo("\nCached Images:")
        click.echo("-" * 80)
        
        for row in result:
            click.echo(f"ASIN: {row.asin}")
            click.echo(f"URL: {row.image_url}")
            click.echo(f"Updated: {row.last_updated}")
            click.echo("-" * 80)
        
        # Show stats
        stats = conn.execute(text("SELECT COUNT(*) as total FROM product_images")).scalar()
        click.echo(f"\nTotal cached images: {stats}")

if __name__ == '__main__':
    show_cached_images() 