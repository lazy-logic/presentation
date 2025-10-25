from nicegui import ui

def footer():
    # Add brand fonts and icon protection
    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        /* Brand typography - excludes icons to prevent font override */
        *:not(.material-icons):not(.q-icon):not([class*="material-icons"]):not(i) {
            font-family: 'Raleway', sans-serif !important;
        }

        /* Material Icons properties */
        .material-icons {
            font-family: 'Material Icons' !important;
            font-weight: normal;
            font-style: normal;
            font-size: 24px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
            -webkit-font-feature-settings: 'liga';
        }

        /* Ensure footer styling takes precedence */
        footer {
            background-color: #1f2937 !important;
            color: white !important;
        }

        /* Typography classes */
        .heading-1 { font-size: 3rem; font-weight: 700; line-height: 1.1; }
        .heading-2 { font-size: 2.25rem; font-weight: 600; line-height: 1.2; }
        .sub-heading { font-size: 1.5rem; font-weight: 500; line-height: 1.4; }
        .body-text { font-size: 1rem; font-weight: 400; line-height: 1.6; }
        .button-label { font-size: 0.875rem; font-weight: 600; }
        .caption { font-size: 0.75rem; font-weight: 400; }

        /* Brand colors */
        .brand-primary { color: #0055B8; }
        .brand-charcoal { color: #1A1A1A; }
        .brand-slate { color: #4D4D4D; }
        .brand-light-mist { background-color: #F2F7FB; }
        .brand-primary-bg { background-color: #0055B8; }
        
        /* Footer Responsive Styles */
        footer {
            min-height: 64px;
            height: auto !important;
        }
        
        .footer-links {
            display: flex;
            gap: 1rem;
        }
        
        .footer-social {
            display: flex;
            gap: 1rem;
        }
        
        .footer-copyright {
            display: block;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            footer {
                flex-direction: column !important;
                padding: 1.5rem 1rem !important;
                gap: 1rem !important;
                text-align: center;
            }
            
            .footer-links {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .footer-copyright {
                font-size: 0.75rem !important;
                order: 3;
            }
            
            .footer-social {
                order: 2;
                justify-content: center;
            }
        }
        
        @media (max-width: 480px) {
            footer {
                padding: 1rem 0.75rem !important;
            }
            
            .footer-links {
                font-size: 0.75rem !important;
            }
        }
    </style>
    ''')
    with ui.element('footer').classes('flex items-center justify-between w-full px-4 text-white').style('background-color: #1f2937 !important; color: white !important; min-height: 64px; padding: 1rem;'):
        # Logo section
        with ui.row().classes('items-center gap-3'):
            ui.icon('hub', size='1.5rem').style('color: #0055B8 !important;')
            ui.label('Dompell').classes('text-lg font-semibold text-white').style('font-family: "Raleway", sans-serif;')
        ui.label('© 2025 Dompell Africa. All rights reserved.').classes('text-sm footer-copyright')
        with ui.row().classes('footer-links'):
            ui.link('Privacy Policy', '#').classes('text-sm no-underline').style('color: white !important; text-decoration: none;').props('hover:text-gray-300')
            ui.link('Terms of Service', '#').classes('text-sm no-underline').style('color: white !important; text-decoration: none;').props('hover:text-gray-300')
        with ui.row().classes('footer-social'):
            ui.html('<a class="social-link" href="#" style="color: #1877F2 !important; transition: opacity 0.2s;" onmouseover="this.style.opacity=\'0.7\'" onmouseout="this.style.opacity=\'1\'"><svg aria-hidden="true" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24"><path clip-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" fill-rule="evenodd"></path></svg></a>', sanitize=lambda s: s)
            ui.html('<a class="social-link" href="#" style="color: #1DA1F2 !important; transition: opacity 0.2s;" onmouseover="this.style.opacity=\'0.7\'" onmouseout="this.style.opacity=\'1\'"><svg aria-hidden="true" class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.71v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path></svg></a>', sanitize=lambda s: s)
            
