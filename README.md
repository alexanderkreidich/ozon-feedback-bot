# Ozon Comment Bot

Automated bot for responding to customer reviews on Ozon marketplace using AI-generated responses.

## Features

- Monitors unprocessed reviews on Ozon marketplace
- Generates contextual responses using DeepSeek AI
- Prevents duplicate responses with SQLite database tracking
- Configurable rate limiting and processing intervals
- Comprehensive logging and error handling

## Requirements

- Python 3.8+
- Ozon Seller Premium Plus subscription (required for review API access)
- DeepSeek API access

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ozon-comment-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment configuration:
```bash
cp .env.example .env
```

4. Configure your API credentials in `.env`:
```bash
OZON_CLIENT_ID=your_client_id_here
OZON_API_KEY=your_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

## Configuration

Edit `.env` file with your settings:

- `OZON_CLIENT_ID`: Your Ozon Client ID from seller profile
- `OZON_API_KEY`: Your Ozon API Key from seller profile  
- `DEEPSEEK_API_KEY`: Your DeepSeek API key
- `BOT_RUN_INTERVAL`: Seconds between processing cycles (default: 3600)
- `MAX_RESPONSES_PER_HOUR`: Maximum responses per hour (default: 10)
- `MARK_AS_PROCESSED`: Mark reviews as processed after responding (default: true)

## Usage

Run the bot:
```bash
cd src
python main.py
```

The bot will:
1. Check for unprocessed reviews every hour (configurable)
2. Generate appropriate responses using AI
3. Post responses to Ozon
4. Track processed reviews in database
5. Log all activities

## API Requirements

### Ozon Seller API
- Requires Premium Plus subscription
- Get credentials from: https://seller.ozon.ru/app/settings/api-keys

### DeepSeek API  
- Sign up at: https://platform.deepseek.com/
- Get API key from dashboard

## Directory Structure

```
ozon-comment-bot/
├── src/
│   ├── main.py              # Bot entry point
│   ├── config.py            # Configuration manager
│   ├── database/
│   │   ├── manager.py       # Database operations
│   │   └── schema.sql       # Database schema
│   ├── clients/
│   │   ├── ozon_client.py   # Ozon API client
│   │   └── deepseek_client.py # AI client
│   └── utils/
│       └── logger.py        # Logging utilities
├── data/                    # Database storage
├── logs/                    # Application logs
└── requirements.txt
```

## Logging

Logs are stored in `logs/` directory with daily rotation. Check logs for:
- Processing status
- API responses  
- Error details
- Performance metrics

## Safety Features

- Rate limiting prevents API overuse
- Database prevents duplicate responses
- Fallback responses for AI failures
- Comprehensive error handling
- Hourly response limits

## Troubleshooting

1. **API Authentication Errors**: Verify credentials in `.env`
2. **Premium Plus Required**: Review list endpoint needs Premium Plus subscription
3. **Rate Limiting**: Adjust `MAX_RESPONSES_PER_HOUR` if hitting limits
4. **Database Issues**: Check `.data/` directory permissions

## Support

For issues and feature requests, please check the logs first and ensure all configuration is correct.