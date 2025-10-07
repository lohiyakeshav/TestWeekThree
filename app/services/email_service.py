import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.core.logger import log_action

class EmailService:
    @staticmethod
    @log_action("send_email")
    def send_email(to_email: str, subject: str, html_content: str):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        try:
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
    
    @staticmethod
    def send_success_email(to_email: str):
        html_content = """
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width,initial-scale=1">
          <title>Payment Successful</title>
        </head>
        <body style="margin:0;padding:0;background:#f4f6f8;font-family:Helvetica,Arial,sans-serif;">
          <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
            <tr>
              <td align="center" style="padding:20px 10px;">
                <table role="presentation" cellpadding="0" cellspacing="0" width="600" style="background:#ffffff;border-radius:8px;overflow:hidden;">
                  <tr>
                    <td style="background:#0f62fe;padding:20px 30px;color:#ffffff;text-align:center;">
                      <h1 style="margin:0;font-size:22px;font-weight:600;">Order Successful!</h1>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:30px;text-align:center;">
                      <p style="margin:0 0 15px;font-size:16px;color:#0b1726;">Thank you for your order. Your transaction has been successfully processed.</p>
                      <p style="margin:0 0 25px;font-size:15px;color:#334155;">We appreciate your business and hope to serve you again soon.</p>
                    </td>
                  </tr>
                  <tr>
                    <td style="background:#f8fafc;padding:16px 30px;color:#7b8794;font-size:13px;text-align:center;">
                      <p style="margin:0;">Thank you for choosing our service.</p>
                      <p style="margin:8px 0 0;font-size:12px;color:#94a3b8;">This is an automated message — please do not reply.</p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """
        EmailService.send_email(to_email, "Order Successful", html_content)
    
    @staticmethod
    def send_failure_email(to_email: str):
        html_content = """
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width,initial-scale=1">
          <title>Order Failed</title>
        </head>
        <body style="margin:0;padding:0;background:#f4f6f8;font-family:Helvetica,Arial,sans-serif;">
          <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
            <tr>
              <td align="center" style="padding:20px 10px;">
                <table role="presentation" cellpadding="0" cellspacing="0" width="600" style="background:#ffffff;border-radius:8px;overflow:hidden;">
                  <tr>
                    <td style="background:#ff4d4f;padding:20px 30px;color:#ffffff;text-align:center;">
                      <h1 style="margin:0;font-size:22px;font-weight:600;">Order Failed</h1>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:30px;text-align:center;">
                      <p style="margin:0 0 15px;font-size:16px;color:#0b1726;">Unfortunately, your order could not be processed at this time.</p>
                      <p style="margin:0 0 25px;font-size:15px;color:#334155;">Please try again later or contact support if the issue persists.</p>
                    </td>
                  </tr>
                  <tr>
                    <td style="background:#f8fafc;padding:16px 30px;color:#7b8794;font-size:13px;text-align:center;">
                      <p style="margin:0;">Need help? Contact our support team.</p>
                      <p style="margin:8px 0 0;font-size:12px;color:#94a3b8;">This is an automated message — please do not reply.</p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """
        EmailService.send_email(to_email, "Order Failed", html_content)
