# SO CRM Module

This module is a standalone CRM (Customer Relationship Management) system for SyncedOffice, replicated from ERPNext CRM.

## Features

- **Lead Management**: Track and manage leads through the sales pipeline
- **Opportunity Management**: Convert leads to opportunities and track deal progress
- **Prospect Management**: Manage potential customers and their information
- **Campaign Management**: Create and track marketing campaigns
- **Contract Management**: Handle customer contracts and agreements
- **Appointment Booking**: Schedule and manage appointments with leads/customers
- **Reports & Analytics**: Various reports for sales pipeline, lead conversion, and campaign efficiency

## DocTypes

### Core DocTypes
- **Lead**: Individual or organization contact information
- **Opportunity**: Sales opportunity with items and stages
- **Prospect**: Potential customer organization
- **Campaign**: Marketing campaign tracking
- **Contract**: Customer contract management
- **Appointment**: Scheduled appointments

### Supporting DocTypes
- **CRM Settings**: Module configuration
- **CRM Note**: Notes for CRM records
- **Sales Stage**: Opportunity pipeline stages
- **Opportunity Type**: Categorization of opportunities
- **Market Segment**: Market segmentation
- **Competitor**: Competitor information
- **Lost Reason**: Reasons for lost opportunities

### Child Tables
- **Opportunity Item**: Line items in opportunities
- **Prospect Lead**: Links between prospects and leads
- **Prospect Opportunity**: Links between prospects and opportunities
- **Campaign Email Schedule**: Email scheduling for campaigns
- **Contract Fulfilment Checklist**: Contract requirements tracking

## Reports

1. **Lead Details**: Comprehensive lead information
2. **Lead Conversion Time**: Track how long leads take to convert
3. **Lead Owner Efficiency**: Performance metrics for lead owners
4. **Sales Pipeline Analytics**: Visual pipeline analysis
5. **Opportunity Summary by Sales Stage**: Opportunities grouped by stage
6. **Lost Opportunity**: Analysis of lost deals
7. **Campaign Efficiency**: Campaign performance metrics
8. **First Response Time for Opportunity**: Response time tracking
9. **Prospects Engaged but Not Converted**: Follow-up opportunities

## Dashboard Charts

- Incoming Leads
- Lead Source
- Opportunity Trends
- Won Opportunities
- Territory Wise Opportunity Count
- Territory Wise Sales
- Opportunities via Campaigns

## Dependencies

**Note**: This module has dependencies on other ERPNext modules that need to be ported or implemented:

### Required Modules
- `syncedoffice.accounts.party` - Party (Customer/Supplier) management
- `syncedoffice.selling.doctype.customer.customer` - Customer DocType
- `syncedoffice.controllers.selling_controller` - Base selling controller
- `syncedoffice.controllers.accounts_controller` - Accounts controller
- `syncedoffice.setup.utils` - Setup utilities (exchange rates, etc.)
- `syncedoffice.utilities.transaction_base` - Base transaction class
- `syncedoffice.tests.utils` - Test utilities

### Optional Dependencies
These are used in some features but the module can function without them:
- Quotation DocType (for converting opportunities)
- Customer DocType (for converting leads)
- Address and Contact DocTypes (for party information)

## Installation

1. The module has been added to `modules.txt` as "SO CRM"
2. Run bench migrate to install the doctypes:
   ```bash
   bench --site [site-name] migrate
   ```

## Configuration

After installation, configure the module through:
- **CRM Settings**: Set default values and behavior
- **Sales Stages**: Define your sales pipeline stages
- **Opportunity Types**: Configure opportunity categories

## Usage

### Creating a Lead
1. Go to SO CRM > Lead > New
2. Fill in contact information
3. Assign to a lead owner
4. Track through the pipeline

### Converting Lead to Opportunity
1. Open a Lead
2. Click "Create" > "Opportunity"
3. Add opportunity items and details
4. Track through sales stages

### Creating Campaigns
1. Go to SO CRM > Campaign > New
2. Set campaign details
3. Schedule email campaigns if needed
4. Track campaign efficiency through reports

## Customization

All naming references have been updated from "ERPNext" to "SyncedOffice" and the module name is "SO CRM" to maintain consistency with other SyncedOffice modules.

## Future Enhancements

To make this module fully functional, you will need to:
1. Implement or port the required dependencies listed above
2. Create Customer, Quotation, and other related doctypes
3. Implement the selling and accounts controllers
4. Set up proper permissions and workflows
5. Configure email templates for campaigns

## Support

For issues or questions, please refer to the SyncedOffice documentation or contact support.
