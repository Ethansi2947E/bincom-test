import os
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Fixes the SQLite database schema by adding missing columns'

    def handle(self, *args, **options):
        # Only run this command for SQLite
        if settings.USE_MYSQL == 'True':
            self.stdout.write(self.style.WARNING('This command is only for SQLite databases. Skipping...'))
            return

        self.stdout.write(self.style.SUCCESS('Starting SQLite schema fix...'))
        
        # Check if we're using SQLite
        if connection.vendor != 'sqlite':
            self.stdout.write(self.style.WARNING('This command is only for SQLite databases. Skipping...'))
            return
        
        # Get the cursor
        cursor = connection.cursor()
        
        # Check if party table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='party'")
        if not cursor.fetchone():
            self.stdout.write(self.style.WARNING('Creating party table...'))
            try:
                cursor.execute("""
                CREATE TABLE party (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    party_id VARCHAR(50),
                    party_name VARCHAR(100),
                    party_abbreviation VARCHAR(50)
                )
                """)
                
                # Insert some default parties
                parties = [
                    ('1', 'People\'s Democratic Party', 'PDP'),
                    ('2', 'Action Congress of Nigeria', 'ACN'),
                    ('3', 'All Nigeria Peoples Party', 'ANPP'),
                    ('4', 'Congress for Progressive Change', 'CPC'),
                    ('5', 'Labour Party', 'LP'),
                ]
                
                cursor.executemany(
                    "INSERT INTO party (party_id, party_name, party_abbreviation) VALUES (?, ?, ?)",
                    parties
                )
                
                self.stdout.write(self.style.SUCCESS('Successfully created party table with default parties!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating party table: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('party table already exists.'))
        
        # Check if uniquewardid column exists in polling_unit table
        cursor.execute("PRAGMA table_info(polling_unit)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'uniquewardid' not in columns:
            self.stdout.write(self.style.WARNING('Adding uniquewardid column to polling_unit table...'))
            try:
                cursor.execute("ALTER TABLE polling_unit ADD COLUMN uniquewardid VARCHAR(50) NULL")
                self.stdout.write(self.style.SUCCESS('Successfully added uniquewardid column!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding uniquewardid column: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('uniquewardid column already exists in polling_unit table.'))
        
        # Check if uniqueid column exists in polling_unit table
        if 'uniqueid' not in columns:
            self.stdout.write(self.style.WARNING('Adding uniqueid column to polling_unit table...'))
            try:
                cursor.execute("ALTER TABLE polling_unit ADD COLUMN uniqueid INTEGER NULL")
                
                # Update uniqueid values based on polling_unit_id
                cursor.execute("UPDATE polling_unit SET uniqueid = polling_unit_id")
                
                self.stdout.write(self.style.SUCCESS('Successfully added and populated uniqueid column!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding uniqueid column: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('uniqueid column already exists in polling_unit table.'))
        
        # Now check the announced_pu_results table
        cursor.execute("PRAGMA table_info(announced_pu_results)")
        pu_results_columns = [column[1] for column in cursor.fetchall()]
        
        # Check if polling_unit_id column exists in announced_pu_results table
        if 'polling_unit_id' not in pu_results_columns:
            self.stdout.write(self.style.WARNING('Adding polling_unit_id column to announced_pu_results table...'))
            try:
                cursor.execute("ALTER TABLE announced_pu_results ADD COLUMN polling_unit_id INTEGER NULL")
                
                # Check if there's a polling_unit column in the results table
                cursor.execute("PRAGMA table_info(announced_pu_results)")
                result_columns = [column[1] for column in cursor.fetchall()]
                
                # If there's a polling_unit_uniqueid column, use that to update polling_unit_id
                if 'polling_unit_uniqueid' in result_columns:
                    self.stdout.write(self.style.WARNING('Updating polling_unit_id values from polling_unit_uniqueid...'))
                    cursor.execute("UPDATE announced_pu_results SET polling_unit_id = polling_unit_uniqueid")
                
                self.stdout.write(self.style.SUCCESS('Successfully added polling_unit_id column to announced_pu_results!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding polling_unit_id column: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('polling_unit_id column already exists in announced_pu_results table.'))
        
        # Fix foreign key constraints
        self.stdout.write(self.style.WARNING('Fixing foreign key constraints...'))
        try:
            # Disable foreign key checks temporarily
            cursor.execute("PRAGMA foreign_keys = OFF")
            
            # Get all valid polling_unit_id values from polling_unit table
            cursor.execute("SELECT polling_unit_id FROM polling_unit")
            valid_polling_unit_ids = [row[0] for row in cursor.fetchall()]
            
            # Get all announced_pu_results records
            cursor.execute("SELECT result_id, polling_unit_id FROM announced_pu_results")
            results = cursor.fetchall()
            
            # Check for invalid polling_unit_id values and fix them
            invalid_results = []
            for result_id, pu_id in results:
                if pu_id not in valid_polling_unit_ids:
                    invalid_results.append((result_id, pu_id))
            
            if invalid_results:
                self.stdout.write(self.style.WARNING(f'Found {len(invalid_results)} results with invalid polling_unit_id values.'))
                
                # Get the first valid polling_unit_id to use as a fallback
                default_pu_id = valid_polling_unit_ids[0] if valid_polling_unit_ids else None
                
                if default_pu_id:
                    # Update invalid polling_unit_id values to use the default
                    for result_id, _ in invalid_results:
                        cursor.execute(
                            "UPDATE announced_pu_results SET polling_unit_id = ? WHERE result_id = ?",
                            (default_pu_id, result_id)
                        )
                    self.stdout.write(self.style.SUCCESS(f'Updated {len(invalid_results)} results to use valid polling_unit_id {default_pu_id}.'))
                else:
                    self.stdout.write(self.style.ERROR('No valid polling_unit_id found to use as fallback.'))
            
            # Create a new announced_pu_results table with correct foreign key
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS announced_pu_results_new (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                polling_unit_id INTEGER,
                party_abbreviation VARCHAR(50),
                party_score INTEGER,
                entered_by_user VARCHAR(50),
                date_entered DATETIME,
                user_ip_address VARCHAR(50),
                FOREIGN KEY (polling_unit_id) REFERENCES polling_unit(polling_unit_id)
            )
            """)
            
            # Copy data from old table to new table
            cursor.execute("""
            INSERT INTO announced_pu_results_new (
                result_id, polling_unit_id, party_abbreviation, party_score, 
                entered_by_user, date_entered, user_ip_address
            )
            SELECT 
                result_id, polling_unit_id, party_abbreviation, party_score, 
                entered_by_user, date_entered, user_ip_address
            FROM announced_pu_results
            """)
            
            # Drop old table and rename new table
            cursor.execute("DROP TABLE announced_pu_results")
            cursor.execute("ALTER TABLE announced_pu_results_new RENAME TO announced_pu_results")
            
            # Re-enable foreign key checks
            cursor.execute("PRAGMA foreign_keys = ON")
            
            self.stdout.write(self.style.SUCCESS('Successfully fixed foreign key constraints!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fixing foreign key constraints: {e}'))
        
        # Commit the changes
        connection.commit()
        
        self.stdout.write(self.style.SUCCESS('SQLite schema fix completed!')) 