using Microsoft.AspNetCore.Mvc;

namespace ImmiAccount.Pages.Applications;

public class NewModel : PageModelBase
{
    public IActionResult OnGet()
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;
        return Page();
    }
}
